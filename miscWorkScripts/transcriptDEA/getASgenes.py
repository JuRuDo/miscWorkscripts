#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Get genes with different number of AS isoforms between conditions.")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input csv table, contains output from compExpTranscripts script")
    parser.add_argument("-o", "--output", type=str, default='.',
                          help="output folder")
    args = parser.parse_args()

    readInfile(args.input, args.output)


def readInfile(path, out):
    out1 = open(out + '/c1.txt', 'w')
    out2 = open(out + '/c2.txt', 'w')

    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if not cells[0] == 'geneID':
                if 1.0 > float(cells[1]) > 0:
                    out1.write(cells[0] + '\n')
                elif 1.0 > float(cells[2]) > 0:
                    out2.write(cells[0] + '\n')
    infile.close()
    out1.close()
    out2.close()


if __name__ == '__main__':
    main()
