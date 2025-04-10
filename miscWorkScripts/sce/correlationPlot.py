#!/bin/env python


import argparse
import scanpy
from scipy.stats.stats import pearsonr
import pandas as pd
import plotly.express as px


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input data as h5ad file.")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output folder.")
    parser.add_argument("-g", "--genes", type=str, default=None, required=True,
                          help="input file with list of genes.")
    args = parser.parse_args()

    adata = scanpy.read_h5ad(args.input)

    genelist = readGenelist(args.genes)
    pearson = {}
    for x in range(len(genelist)):
        for y in range(x+1,len(genelist)):
            df = pd.DataFrame({
                genelist[x]: list(adata.obs_vector(genelist[x])),
                genelist[y]: list(adata.obs_vector(genelist[y])),
                'Patient': list(adata.obs['Patient'])
            })
            pearson[genelist[x] + '#' + genelist[y]] = pearsonr(list(df[genelist[x]]), list(df[genelist[y]]))
            fig = px.scatter(df, x=genelist[x], y=genelist[y], trendline='ols')
            fig.update_traces(marker=dict(size=3,))
            fig.write_image(args.output + '/' + genelist[x] + '#' + genelist[y] + '.svg')
    with open(args.output + '/pearson.csv', 'w') as out:
        out.write('Genes\tcoefficient\tpval\n')
        for i in pearson:
            out.write(i + '\t' + str(pearson[i][0]) + '\t' + str(pearson[i][1]) + '\n')
    out.close()


def readGenelist(path):
    infile = open(path, 'r')
    genelist = []
    for line in infile.readlines():
        genelist.append(line.rstrip('\n'))
    infile.close()
    return genelist



if __name__ == '__main__':
    main()
