#!/bin/env python


import argparse
import scanpy


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input data as h5ad file.")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    args = parser.parse_args()

    adata = scanpy.read_h5ad(args.input)

    adata.obs['Module'] = 'None'
    for i in range(len(adata.obs['Module Secretory Intestine Score'])):
        mtils = adata.obs['Module Tumor ISC-like Score'].iloc[i] < 1
        msis = adata.obs['Module Secretory Intestine Score'].iloc[i] < 1
        mss = adata.obs['Module Squamous Score'].iloc[i] < 1
        mis = adata.obs['Module Intestine Score'].iloc[i] < 1
        meds = adata.obs['Module Endoderm Development Score'].iloc[i] < 1
        mirs = adata.obs['Module Injury Repair Score'].iloc[i] < 1
        mns = adata.obs['Module Neuroendocrine Score'].iloc[i] < 1
        mais = adata.obs['Module Absorptive Intestine Score'].iloc[i] < 1
        mos = adata.obs['Module Osteoblast Score'].iloc[i] < 1
        if (not mtils) and msis and mss and mis and meds and mirs and mns and mais and mos:
            adata.obs['Module'].iloc[i] = 'Tumor ISC-like'
        elif mtils and (not msis) and mss and mis and meds and mirs and mns and mais and mos:
            adata.obs['Module'].iloc[i] = 'Secretory Intestine'
        elif mtils and msis and (not mss) and mis and meds and mirs and mns and mais and mos:
            adata.obs['Module'].iloc[i] = 'Squamous'
        elif mtils and msis and mss and (not mis) and meds and mirs and mns and mais and mos:
            adata.obs['Module'].iloc[i] = 'Intestine'
        elif mtils and msis and mss and mis and (not meds) and mirs and mns and mais and mos:
            adata.obs['Module'].iloc[i] = 'Endoderm Development'
        elif mtils and msis and mss and mis and meds and (not mirs) and mns and mais and mos:
            adata.obs['Module'].iloc[i] = 'Injury Repair'
        elif mtils and msis and mss and mis and meds and mirs and (not mns) and mais and mos:
            adata.obs['Module'].iloc[i] = 'Neuroendocrine'
        elif mtils and msis and mss and mis and meds and mirs and mns and (not mais) and mos:
            adata.obs['Module'].iloc[i] = 'Absorptive Intestine'
        elif mtils and msis and mss and mis and meds and mirs and mns and mais and (not mos):
            adata.obs['Module'].iloc[i] = 'Osteoblast'
    scanpy.write(args.output, adata)


if __name__ == '__main__':
    main()
