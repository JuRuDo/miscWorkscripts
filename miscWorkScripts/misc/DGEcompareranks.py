#!/bin/env python

import argparse
import scipy.stats as stats


def main():
    parser = argparse.ArgumentParser(description="Get all entries in column x that reach threshold t in column y")
    parser.add_argument("-x", "--t1", type=str, default=None, required=True,
                          help="input table in tsv format")
    parser.add_argument("-y", "--t2", type=str, default=None, required=True,
                          help="input table in tsv format")
    args = parser.parse_args()

    r1 = readRanking(args.t1)
    r2 = readExp(args.t2)
    r1, r2 = removeMissing(r1, r2)
    x = stats.kendalltau(r1, r2, nan_policy='raise')
    print('tau: ' + str(x.statistic) + '\np_value: ' + str(x.pvalue))


def readRanking(path):
    ranks = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[0] == 'Negativenames':
                ranks.append(cells[5])
    return ranks


def readExp(path):
    ranks = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if not cells[0] == 'gene_name':
                try:
                    tmp = float(cells[2])/float(cells[1])
                except:
                    tmp = 0.0
                ranks.append((cells[0], tmp))
    ranks.sort(key=lambda a: a[1])
    finalranks = []
    for i in ranks:
        finalranks.append(i[0])
    return finalranks


def removeMissing(r1, r2):
    new_r1, new_r2 = [], []
    for i in r1:
        if i in r2:
            new_r1.append(i)
    for i in r2:
        if i in new_r1:
            new_r2.append(i)
    return new_r1, new_r2


if __name__ == '__main__':
    main()
