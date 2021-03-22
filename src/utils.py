import json
import os
import glob
import csv
import numpy as np
import pandas as pd
import logging
import src.config as config

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)


def _get_file(OUT_DIR, n, header_line):
    filename = os.path.basename(OUT_DIR).split('.')[0]
    file = os.path.join(OUT_DIR, filename + '_%d.%s' % (n, 'tsv'))
    handle = open(file, "a", newline='', encoding='utf-8')
    write = csv.writer(handle, delimiter='\t')
    write.writerow(header_line)
    return file, handle

def splitter_mb(df, dir_path, mb_size):
    """ Splits a text file in (almost) equally sized parts on the disk. Assumes that there is a header in the first line
    :param filepath: The path of the text file to be broken up into smaller files
    :param mb_size: size in MB of each chunk
    :return:
    """
    # OUT_DIR = os.path.join(os.path.splitext(filepath)[0] + '_split')

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        files = glob.glob(dir_path + '/*.*')
        for f in files:
            os.remove(f)

    n = 0
    header_line = df.columns.tolist()
    # header_line = next(handle)[1].tolist()
    file_out, handle_out = _get_file(dir_path, n, header_line)
    # data_row = next(handle)[1].tolist()
    for index, row in df.iterrows():
        row = row.tolist()
        size = os.stat(file_out).st_size
        if size > mb_size*1024*1024:
            logger.info('saved %s with file size %4.3f MB' % (file_out, size/(1024*1024)))
            n += 1
            handle_out.close()
            file_out, handle_out = _get_file(dir_path, n, header_line)
        write = csv.writer(handle_out, delimiter='\t')
        write.writerow(row)

    # print(str(file_out) + " file size = \t" + str(size))
    logger.info('saved %s with file size %4.3f MB' % (file_out, size / (1024 * 1024)))
    handle_out.close()


def transformation(cgf):
    with open(cgf['manifest']) as f:
        settings = json.load(f)

    # bounding box in microns
    bbox = {}
    bbox['x0'] = settings['bbox_microns'][0]
    bbox['x1'] = settings['bbox_microns'][2]

    bbox['y0'] = settings['bbox_microns'][1]
    bbox['y1'] = settings['bbox_microns'][3]

    # image width and height in pixels
    img = {}
    img['width'] = settings['mosaic_width_pixels']
    img['height'] = settings['mosaic_height_pixels']

    # Affine transformation: a set of coefficients a, b, c, d for transforming a point of a form (x, y) into (a*x + b, c*y + d)
    a = img['width'] / (bbox['x1'] - bbox['x0'])
    b = -1 * img['width'] / (bbox['x1'] - bbox['x0']) * bbox['x0']
    c = img['height'] / (bbox['y1'] - bbox['y0'])
    d = -1 * img['height'] / (bbox['y1'] - bbox['y0']) * bbox['y0']

    tx = lambda x: a * x + b
    ty = lambda y: c * y + d

    return tx, ty

if __name__=="__main__":
    cfg = config.DEFAULT
    tx, ty = transformation(cfg)

    spots_path = cfg['detected_transcripts']
    chunks = pd.read_csv(spots_path, chunksize=100000)
    data = pd.concat(chunks)
    data.shape


    data_z3 = data[data.global_z == 3]
    [unique_gene_names, gene_id, counts_per_gene] = np.unique(data_z3.gene.values, return_inverse=True,
                                                              return_counts=True)
    data_z3 = data_z3[['gene', 'global_x', 'global_y']].rename(
        columns={'gene': "Gene", 'global_x': "x", 'global_y': "y"})

    data_z3['Gene_id'] = gene_id
    data_z3['neighbour'] = np.zeros(len(gene_id))
    data_z3['neighbour_array'] = [[0] for i in range(len(gene_id))]
    data_z3['neighbour_prob'] = [[1.0] for i in range(len(gene_id))]

    splitter_mb(data_z3, 'geneData', 99)
    logger.info('Done!')





