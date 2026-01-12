#!/bin/env python

import argparse
from scipy.stats import pearsonr


def main():
    parser = argparse.ArgumentParser(description="Pearson correlation between to sets of data")
    parser.add_argument("--m1", type=str, default=None, required=True,
                        help="input csv file 1")
    parser.add_argument("--m2", type=str, default=None, required=True,
                        help="input csv file 2")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                        help="output directory")
    args = parser.parse_args()

    set1 = readSet(args.m1)
    set2 = readSet(args.m2)
    cor, pval = calcPearson(set1, set2)
    outWrite(cor, pval, args.output, list(set2.keys()))


def readSet(path):
    with open(path, 'r') as infile:
        sets = {}
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if not cells[0] == "SYMBOL":
                sets[cells[0]] = []
                for i in cells[1:]:
                    sets[cells[0]].append(float(i))
        infile.close()
    return sets


def calcPearson(set1, set2):
    cor = {}
    pval = {}
    for x in set1:
        cor_tmp = []
        pval_tmp = []
        for y in set2:
            p = pearsonr(set1[x], set2[y])
            cor_tmp.append(str(p[0]))
            pval_tmp.append(str(p[1]))
        cor[x] = cor_tmp
        pval[x] = pval_tmp
    return cor, pval


def outWrite(cor, pval, path, set2):
    cor_out = open(path + '/pearson_correlation.csv', 'w')
    pval_out = open(path + '/pearson_pvalue.csv', 'w')
    cor_out.write('\t' + '\t'.join(set2) + '\n')
    pval_out.write('\t' + '\t'.join(set2) + '\n')
    for x in cor:
        cor_out.write(x + '\t' + '\t'.join(cor[x]) + '\n')
        pval_out.write(x + '\t' + '\t'.join(pval[x]) + '\n')
    cor_out.close()
    pval_out.close()


if __name__ == '__main__':
    main()
