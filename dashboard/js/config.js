function config() {
    return {
            roi: {"x0": -5071.627079999999, "x1": 4622.530679999998, "y0": -6427.59084, "y1": 221.184 },
            imageSize: [262144, 179792],
            tiles: 'maptiles/262144px/z3/{z}/{y}/{x}.jpg',
            cellData: 'https://api.github.com/repos/acycliq/VS6_MsBrain_A3/contents/dashboard/data/cellData?ref=main',
            geneData: 'https://api.github.com/repos/acycliq/VS6_MsBrain_A3/contents/dashboard/data/geneData?ref=main',
            cellCoords: 'https://api.github.com/repos/acycliq/VS6_MsBrain_A3/contents/dashboard/data/cellCoords?ref=main',
            class_name_separator: '.' //The delimiter in the class name string, eg if name is Astro.1, then use the dot as a separator, if Astro1 then use an empty string. It is used in a menu/control to show the class names nested under its broader name
        }
}
