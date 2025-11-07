#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Get length of all transcripts")
    parser.add_argument("-f", "--fasta", type=str, default=None, required=True,
                        help="input fasta")
    parser.add_argument("-l", "--genelist", type=str, default=None, required=True,
                        help="input list with uniprot identifiers")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                        help="output fasta")
    args = parser.parse_args()

    genes = readGeneList(args.genelist)
    data = readFasta(args.fasta)
    writeOutfile(args.output, data, genes)


def readGeneList(path):
    genes = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            genes.append(line.rstrip('\n'))
    infile.close()
    return genes


def readFasta(path):
    data = {}
    with open(path, 'r') as infile:
        line = infile.readline()
        header = None
        seq = ''
        while line:
            if line[0] == '>':
                if header:
                    data[header] = seq
                cells = line.split('|')
                header = cells[1]
                seq = ''
            else:
                seq += line.rstrip('\n')
            line = infile.readline()
    infile.close()
    return data


def writeOutfile(path, data, genes):
    with open(path, 'w') as out:
        for gene in genes:
            if gene in data:
                out.write('>' + gene + '\n' + data[gene] + '\n')
            else:
                print(gene)
    out.close()


if __name__ == '__main__':
    main()
