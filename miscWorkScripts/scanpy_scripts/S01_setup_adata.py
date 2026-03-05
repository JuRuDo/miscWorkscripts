#!/bin/env python


import argparse
import scanpy as sc
import anndata as ad
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True, nargs='+',
                          help="input directory with 10x matrix")
    parser.add_argument("-m", "--meta", type=str, default=None,
                        help="input csv file with meta data")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    args = parser.parse_args()

    adata = read10x_data(args.input)
    adata = read_meta(args.meta, adata)
    sc.write(args.output, adata)


def read10x_data(paths):
    ad_list = []
    for path in paths:
        tmp = sc.read_10x_mtx(path)
        tmp.obs["Sample"] = path.split("/")[-2]
        ad_list.append(tmp)
    adata = ad.concat(ad_list)
    adata.obs_names_make_unique()
    return adata


def read_meta(path, adata):
    df = pd.read_csv(path, index_col=0, delimiter="\t")
    for obs in df.columns:
        adata.obs[obs] = None
        for key in df.index:
            adata.obs.loc[adata.obs["Sample"] == key, obs] = df[obs][key]
    return adata


if __name__ == '__main__':
    main()
