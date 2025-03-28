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
                          help="Colorscale.")
    parser.add_argument("-b", "--groupby", type=str, default='Sample Type', required=False,
                          help="Group samples by.")
    parser.add_argument("-f", "--filter", type=str, required=False,
                          help="Filter by.")
    parser.add_argument("-l", "--filter2", type=str, required=False,
                          help="If --filter is on use this for the arg")
    args = parser.parse_args()

    adata = scanpy.read_h5ad(args.input)
    infile = open(args.genes, 'r')
    genelist = []
    for line in infile.readlines():
        genelist.append(line.rstrip('\n'))
    infile.close()
    newadata = adata[adata.obs['celltypist_cell_label_fine'] == 'Epithelial cells']
    if args.filter:
        f = args.filter2
        if args.filter2.isnumeric():
            f = int(f)
        newadata = newadata[newadata.obs[args.filter] == f]
        scanpy.pl.heatmap(newadata, genelist, args.groupby, use_raw=False, save=args.output, cmap=args.colors)
    else:
        scanpy.pl.heatmap(newadata, genelist, args.groupby, use_raw=False, save=args.output, cmap=args.colors, show_gene_labels=True)


if __name__ == '__main__':
    main()