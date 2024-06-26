#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Add gene name to table")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="input table in tsv format")
    parser.add_argument("-m", "--map", type=str, default=None, required=True,
                          help="ENS to gene name table. Tab seperated")
    parser.add_argument("-d", "--delimiter", type=str, default=',',
                          help="table delimiter")
    args = parser.parse_args()

    mapping = read_mapping(args.map)
    add_genename(args.infile, mapping, args.delimiter)


def read_mapping(path):
    mapping = {}
    print('NoNanme genes:')
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if cells[1] == '':
                print(cells[0])
            else:
                mapping[cells[0]] = cells[1]
    return mapping


def add_genename(path, mapping, delimiter):
    out = open('.'.join(path.split('.')[0:-1]) + '_geneNames.gct', 'w')
    out.write('#1.2\n')
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(delimiter)
            if cells[0] == 'NAME':
                out.write(str(len(mapping)) + '\t' + str(len(cells[1:])) + '\n')
                tmp = 'NAME\tDESCRIPTION\t' + '\t'.join(cells[1:]) + '\n'
            elif cells[0] in mapping:
                tmp = mapping[cells[0]] + '\tNA\t' + '\t'.join(cells[1:]) + '\n'
            else:
                tmp = ''
            out.write(tmp)
    out.close()
    infile.close()


if __name__ == '__main__':
    main()
