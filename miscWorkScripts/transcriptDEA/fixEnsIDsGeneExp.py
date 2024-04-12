#!/bin/env python

import argparse
import math

def main():
    parser = argparse.ArgumentParser(description="Replace Stringtie Ids with Ensembl Ids")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input csv table, first column should be gene IDs")
    parser.add_argument("-g", "--geneIDs", type=str, default='.',
                          help="tsv table, mapping StringTie gene ID (column 1) to Ensembl ID and gene name")
    parser.add_argument("-o", "--output", type=str, default='.',
                          help="output file")
    args = parser.parse_args()
    print('Working...')
    with open(args.input, 'r') as infile:
        lines = infile.readlines()
    infile.close()
    gidTOens, ensTOname = readgeneIds(args.geneIDs)
    fixIDs(args.output, gidTOens, lines, ensTOname)
    print('done!')

def readgeneIds(path):
    gidTOens = {}
    ensTTname = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            gidTOens[cells[0]] = cells[2]
            ensTTname[cells[2]] = cells[1]
    infile.close()
    return gidTOens, ensTTname

def fixIDs(path, gidTOens, lines, ensTOname):
    with open(path, 'w') as out:
        for line in lines:
            cells = line.rstrip('\n').split(',')
            for i in range(len(cells)):
                cells[i] = cells[i].strip('"')
            if cells[0] == 'id':
                out.write(','.join(['geneNames', 'GeneIDs', 'Log2FoldChange', 'pValue', 'qValue'] + cells[4:]) + '\n')
            else:
                if not cells[1] == 'NA':
                    cells[1] = str(math.log2(float(cells[1])))
                if cells[0] in gidTOens:
                    tmp = [ensTOname[gidTOens[cells[0]]], gidTOens[cells[0]]] + cells[1:]
                elif cells[0] in ensTOname:
                    tmp = [ensTOname[cells[0]], cells[0]] + cells[1:]
                else:
                    tmp = [''] + cells
                out.write(','.join(tmp) + '\n')
    out.close()


if __name__ == '__main__':
    main()
