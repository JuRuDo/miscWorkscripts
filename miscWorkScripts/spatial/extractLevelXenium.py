#!/usr/bin/env python

import tifffile
import argparse



def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="morphology.ome.tif file from xenium pipeline.")
    parser.add_argument("-o", "--out", type=str, default=None, required=True,
                          help="Output directory")
    parser.add_argument("-l", "--level", type=int, default=None, required=True,
                          help="Which image level to extract [0-6].")
    args = parser.parse_args()

    # Variable 'LEVEL' determines the level to extract. It ranges from 0 (highest
    # resolution) to 6 (lowest resolution) for morphology.ome.tif
    LEVEL = args.level

    with tifffile.TiffFile(args.input) as tif:
        image = tif.series[0].levels[LEVEL].asarray()

    tifffile.imwrite(
        args.out+'/level_'+str(LEVEL)+'_morphology.ome.tif',
        image,
        photometric='minisblack',
        dtype='uint16',
        tile=(1024, 1024),
        compression='JPEG_2000_LOSSY',
        metadata={'axes': 'ZYX'},
        bigtiff=True
    )

if __name__ == '__main__':
    main()
