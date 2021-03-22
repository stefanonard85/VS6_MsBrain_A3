import os


ROOT_DIR = os.path.join('E:\\', 'Neuroscience', 'data', 'Stefano', 'aws', 'rawData', 'vz-data-to vs6', 'analyzed_data', 'v1', 'VS6_MsBrain_A3_VS6library_V3_LH_02-07-21')

DEFAULT = {
    'cell_by_gene': os.path.join(ROOT_DIR, 'cell_by_gene.csv'),

    'cell_metadata': os.path.join(ROOT_DIR, 'cell_metadata.csv'),

    'detected_transcripts': os.path.join(ROOT_DIR, 'detected_transcripts.csv'),

    'manifest': os.path.join(ROOT_DIR, 'images', 'manifest.json'),
}

