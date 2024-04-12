#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Get all entries in column x that reach threshold t in column y")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="input table in tsv format")
    parser.add_argument("-x", "--columnx", type=int, default=1,
                          help="column x")
    parser.add_argument("-y", "--columny", type=int, default=2,
                          help="column y")
    parser.add_argument("-t", "--threshold", type=float, default=2.0,
                          help="threshold")
    parser.add_argument("-r", "--relation", type=str, default='>=',
                          help="the type of relation to the trheshold that should be tested, "
                               "options are '>', '<', '>=', '<=' or '=' ")
    args = parser.parse_args()

    read_csv(args.infile, args.columnx, args.columny, args.threshold, args.relation)


def read_csv(path, x, y, t, r):
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if r == '>=':
                if float(cells[y-1]) >= t:
                    print(cells[x-1])
            elif r == '>':
                if float(cells[y-1]) > t:
                    print(cells[x-1])
            elif r == '<':
                if float(cells[y-1]) < t:
                    print(cells[x-1])
            elif r == '<=':
                if float(cells[y-1]) <= t:
                    print(cells[x-1])
            elif r == '=':
                if float(cells[y-1]) == t:
                    print(cells[x-1])
            else:
                raise Exception('relation not defined correctly, check help to see what options are available')
    infile.close()


if __name__ == '__main__':
    main()
