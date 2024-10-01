#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Get length of all transcripts")
    parser.add_argument("-f", "--fasta", type=str, default=None, required=True,
                        help="input fasta")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                        help="output table in csv format")
    args = parser.parse_args()

    data = readInfile(args.fasta)
    writeOutfile(args.output, data)


def readInfile(path):
    data = {}
    with open(path, 'r') as infile:
        line = infile.readline()
        gene = None
        transcript = None
        length = 0
        while line:
            if line[0] == '>':
                if gene:
                    if gene not in data:
                        data[gene] = {}
                    data[gene][transcript] = length
                cells = line.split(' ')
                gene = cells[3].split(':')[1].split('.')[0]
                transcript = cells[4].split(':')[1].split('.')[0]
                length = 0
            else:
                length += len(line.rstrip('\n'))
            line = infile.readline()
    infile.close()
    return data


def writeOutfile(path, data):
    with open(path, 'w') as out:
        for gene in data:
            for transcript in data[gene]:
                out.write(transcript + '\t' + str(data[gene][transcript]) + '\n')


if __name__ == '__main__':
    main()
