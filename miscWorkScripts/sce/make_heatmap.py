#!/bin/env python


import argparse
import scanpy


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input data as h5ad file.")
    parser.add_argument("-g", "--genes", type=str, default=None, required=True,
                          help="input file with list of genes.")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    parser.add_argument("-c", "--colors", type=str, default='turbo', required=False,
                          help="Colorscle.")
    args = parser.parse_args()

    adata = scanpy.read_h5ad(args.input)
    infile = open(args.genes, 'r')
    genelist = []
    for line in infile.readlines():
        genelist.append(line.rstrip('\n'))
    infile.close()
    scanpy.pl.heatmap(adata, genelist, 'leiden_merged', use_raw=True, save=args.output, cmap=args.colors)


if __name__ == '__main__':
    main()