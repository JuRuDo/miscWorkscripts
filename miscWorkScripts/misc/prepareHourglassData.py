#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="create input file for hourglass")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="base input table in csv format")
    parser.add_argument("-g", "--genes", type=str, default=None, required=True,
                          help="file with list of genes")
    parser.add_argument("-1", "--exp1", type=str, default=None, required=True,
                          help="expression File T1")
    parser.add_argument("-2", "--exp2", type=str, default=None, required=True,
                          help="expression File T3")
    parser.add_argument("-o", "--out", type=str, default='hourglass_data.csv',
                          help="output file")
    args = parser.parse_args()

    genes = readGeneList(args.genes)
    exp1 = readExp(args.exp1, genes)
    exp2 = readExp(args.exp2, genes)
    mainTable = readMain(args.infile)
    writeOut(args.out, mainTable, exp1, exp2)


def readGeneList(path):
    genes = []
    with open(path, 'r') as infile:
        for i in infile.readlines():
            genes.append(i.rstrip('\n').upper())
    infile.close()
    return genes


def readExp(path, genes):
    exp = {'genelist': []}
    with open(path, 'r') as infile:
        line = infile.readline()
        cells = line.rstrip('\n').split(',')
        patients = cells[1:]
        for i in patients:
            exp[i] = []
        line = infile.readline()
        while line:
            cells = line.rstrip('\n').split(',')
            gene = cells[0].split('.')[0]
            if gene.upper() in genes:
                exp['genelist'].append(cells[0])
                for i in range(1, len(cells)):
                    exp[patients[i-1]].append(cells[i])
            line = infile.readline()
    infile.close()
    return exp


def readMain(path):
    mainTable = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            mainTable.append(cells)
    infile.close()
    return mainTable


def writeOut(path, mainTable, exp1, exp2):
    with open(path, 'w') as out:
        out.write(','.join(mainTable[0]) + ',' + ','.join(exp1['genelist']) + ',' + ','.join(exp2['genelist']) + '\n')
        for i in range(1, len(mainTable)):
            out.write(','.join(mainTable[i]) + ',' + ','.join(exp1[mainTable[i][0]]) + ',' + ','.join(exp2[mainTable[i][0]]) + '\n')
    out.close()


if __name__ == '__main__':
    main()
