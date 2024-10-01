#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-1", "--htseq1", type=str, default=None, required=True,
                          help="")
    parser.add_argument("-2", "--htseq2", type=str, default=None, required=True,
                          help="")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    args = parser.parse_args()

    htseq1, s1 = readTable(args.htseq1)
    htseq2, s2 = readTable(args.htseq2)
    writeOut(args.output, htseq1, htseq2, s1, s2)



def writeOut(path, htseq1, htseq2, s1, s2):
    genes = set(list(htseq1)).intersection(list(htseq2))
    with open(path, 'w') as out:
        out.write(',' + ','.join(s1) + ',' + ','.join(s2) + '\n')
        for gene in genes:
            out.write(gene + ',' + ','.join(htseq1[gene]) + ',' + ','.join(htseq2[gene]) + '\n')
    out.close()


def readTable(path):
    htseq = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if cells[0] == '':
                samples = cells[1:]
            else:
                htseq[cells[0]] = cells[1:]
    infile.close()
    return htseq, samples


if __name__ == '__main__':
    main()
