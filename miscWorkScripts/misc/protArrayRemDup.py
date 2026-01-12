#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Remove Duplicates from protein exp array")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                        help="input csv file")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                        help="output csv file")
    args = parser.parse_args()
    genes = readInfile(args.input)
    writeOutfile(args.output, genes)


def readInfile(path):
    with open(path) as infile:
        genes = {}
        for line in infile.readlines():
            cells = line.rstrip('\n').split("\t")
            if not cells[0] in genes:
                genes[cells[0]] = cells
        infile.close()
    return genes


def writeOutfile(path, genes):
    with open(path, 'w') as outfile:
        for gene in genes:
            outfile.write('\t'.join(genes[gene]) + '\n')


if __name__ == '__main__':
    main()
