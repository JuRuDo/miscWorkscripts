#!/bin/env python

import argparse
from spatialdata_io import xenium


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input xenium Folder")
    parser.add_argument("-o", "--out", type=str, default=None, required=True,
                          help="Path to out directory.")
    args = parser.parse_args()

    sdata = xenium(args.input)
    sdata.write(args.out + ".zarr")


if __name__ == '__main__':
    main()
