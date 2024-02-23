#!/bin/env python

import argparse

def main():
    parser = argparse.ArgumentParser(description="Replace Stringtie Ids with Ensembl Ids")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input csv table, first columns should be geneNames, geneIDs and transcriptIDs")
    parser.add_argument("-g", "--geneIDs", type=str, default='.',
                          help="tsv table, mapping StringTie gene ID (column 1) to Ensembl ID and gene name")
    parser.add_argument("-o", "--output", type=str, default='.',
                          help="output file")
    args = parser.parse_args()
    print('Working...')
    with open(args.input, 'r') as infile:
        lines = infile.readlines()
    infile.close()
    gidTOens = readgeneIds(args.geneIDs)
    fixIDs(args.output, gidTOens, lines)
    print('done!')

def readgeneIds(path):
    gidTOens = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            gidTOens[cells[0]] = [cells[1], cells[2]]
    infile.close()
    return gidTOens

def fixIDs(path, gidTOens, lines):
    with open(path, 'w') as out:
        for line in lines:
            cells = line.rstrip('\n').split(',')
            for i in range(len(cells)):
                cells[i] = cells[i].strip('"')
            if cells[0] == 'geneNames':
                out.write(','.join(cells) + '\n')
            else:
                if cells[1] in gidTOens:
                    tmp = gidTOens[cells[1]] + cells[2:]
                out.write(','.join(tmp) + '\n')
    out.close


if __name__ == '__main__':
    main()