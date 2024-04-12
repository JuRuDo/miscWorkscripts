#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Filter Rows in a table by a list if IDs")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input table")
    parser.add_argument("-l", "--list", type=str, default='.',
                          help="file with a list of ids used for filtering")
    parser.add_argument("-o", "--output", type=str, default='.',
                          help="output file")
    parser.add_argument("-d", "--delimiter", type=str, default='\t',
                        help="delimiter used in table")
    parser.add_argument("-c", "--column", type=int, default=1,
                        help="column in the table to filter by")

    args = parser.parse_args()
    print('Missing IDs:')
    ids = readIdList(args.list)
    filter(args.input, args.output, args.delimiter, args.column, ids)


def readIdList(path):
    ids = []
    with open(path, 'r')as infile:
        for line in infile.readlines():
            ids.append(line.rstrip('\n').lower())
    infile.close()
    return ids


def filter(inpath, outpath, delimiter, column, ids):
    out = open(outpath, 'w')
    with open(inpath, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(delimiter)
            if cells[column-1].lower() in ids:
                out.write(line)
                ids.remove(cells[column-1].lower())
    infile.close()
    out.close()
    for i in ids:
        print(i)


if __name__ == '__main__':
    main()
