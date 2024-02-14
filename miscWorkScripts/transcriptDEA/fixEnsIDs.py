#!/bin/env python

import argparse

def main():
    parser = argparse.ArgumentParser(description="Combine individual expression tables of samples with output of DEA")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input csv table, first 3 columns should be geneNames, geneIDs and transcriptIDs")
    parser.add_argument("-t", "--TtoG", type=str, default='.',
                          help="tsv table, mapping transcript ID (column 2) to gene ID (column 1)")
    parser.add_argument("-g", "--geneIDs", type=str, default='.',
                          help="tsv table, mapping StringTie gene ID (column 1) to Ensembl ID and gene name")
    parser.add_argument("-o", "--output", type=str, default='.',
                          help="output file")
    args = parser.parse_args()
    print('Working...')
    tTOg = readTtoG(args.TtoG)
    with open(args.input, 'r') as infile:
        lines = infile.readlines()
    infile.close()
    gidTOens = readgeneIds(args.geneIDs)
    gidTOens = createGIDtoENS(lines, tTOg, gidTOens)
    fixIDs(args.output, gidTOens, lines)
    print('done!')

def readTtoG(path):
    tTOg = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            geneID, transcriptID = line.rstrip('\n').split('\t')
            tTOg[transcriptID] = geneID
    infile.close()
    return tTOg

def readgeneIds(path):
    gidTOens = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            gidTOens[cells[0]] = [cells[1], cells[2]]
    infile.close()
    return gidTOens

def createGIDtoENS(lines, tTOg, gidTOens):
    for line in lines:
        cells = line.rstrip('\n').split(',')
        if not cells[0] == '"geneNames"':
            if not cells[1].strip('"') in gidTOens:
                gidTOens[cells[1].strip('"')] = ['.', cells[1].strip('"')]
            if gidTOens[cells[1].strip('"')][0] == '.' and not cells[0] == '"."':
                gidTOens[cells[1].strip('"')][0] = cells[0].strip('"')
            if gidTOens[cells[1].strip('"')][1] == cells[1].strip('"') and cells[2].strip('"') in tTOg:
                gidTOens[cells[1].strip('"')][1] = tTOg[cells[2].strip('"')]
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