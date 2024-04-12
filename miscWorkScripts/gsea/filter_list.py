#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Reads in 2 table and outputs all values in column c1 that have a "
                                                 "descriptor in column c2 that is in a given list")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="input table in tsv format")
    parser.add_argument("--c1", type=int, default=1,
                          help="column containing ids")
    parser.add_argument("--c2", type=int, default=2,
                        help="column containing descriptions")
    parser.add_argument("-x", "--description", type=str, default=None, required=True,
                          help="input list of descriptions")
    parser.add_argument("-d", "--delimiter", type=str, default=',',
                          help="table delimiter")
    args = parser.parse_args()

    desc = read_descriptions(args.descriptions)
    filter_table(args.infile, args.c1, args.c2, desc, args.delimiter)


def read_descriptions(path):
    descriptions = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            descriptions.append(line.rstrip('\n'))
    return descriptions


def filter_table(path, c1, c2, desc, delimiter):
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(delimiter)
            if cells[c2] == 'NAME':
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
