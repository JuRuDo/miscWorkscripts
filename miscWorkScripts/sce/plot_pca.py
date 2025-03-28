#!/bin/env python


import argparse
import scanpy


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input data as h5ad file.")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    parser.add_argument("-c", "--colors", type=str, default='turbo', required=False,
                          help="Colorscale.")
    args = parser.parse_args()

    adata = scanpy.read_h5ad(args.input)
    del adata.obs['Treatment']
#    newadata = adata[adata.obs['Tumor Status'] == 'Primary Tumor']
#    newadata = adata[adata.obs['Sample Type'] == 'Primary']
    scanpy.pl.pca(adata, color=args.colors, save=args.output + '.pdf')


if __name__ == '__main__':
    main()