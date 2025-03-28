#!/bin/env python

import argparse
from operator import itemgetter


def main():
    parser = argparse.ArgumentParser(description="Merge multiple expression table with no headers")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                        help="list of input tables in csv format")
    parser.add_argument("-o", "--outdir", type=str, default=None, required=True,
                        help="output table in tsv format")

    args = parser.parse_args()
    genedata = readInfile(args.infile)
    for entry in genedata:
        writeChr(args.outdir + '/' + entry + '.csv', genedata[entry])


def readInfile(path):
    genedata = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[1] == 'seqnames':
                if not cells[1] in genedata:
                    genedata[cells[1]] = []
                genedata[cells[1]].append((cells[6], int(cells[2]), int(cells[3]), cells[5]))
    infile.close()
    return genedata


def writeChr(path, genedata):
    sortedData = sorted(genedata,key=itemgetter(1))
    with open(path, 'w') as out:
        for entry in sortedData:
            out.write(entry[0] + '\t' + str(entry[1]) + '\t' + str(entry[2]) + '\t' + entry[3] + '\t' + '\n')
    out.close()


if __name__ == '__main__':
    main()
