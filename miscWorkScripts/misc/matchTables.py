#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Add gene name to table")
    parser.add_argument("-x", "--table1", type=str, default=None, required=True,
                        help="input table in tsv format")
    parser.add_argument("-y", "--table2", type=str, default=None, required=True,
                        help="input table in tsv format")
    args = parser.parse_args()

    table_1 = read_table1(args.table1)
    table_2 = read_table2(args.table2)
    merge_tables(table_1, table_2)


def read_table1(path):
    table1 = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            number = int(cells[1])
            mainid = cells[0] + ' | ' + f"{number:03d}" + ' | ' + cells[2]
            table1[mainid] = cells[3:]
    return table1


def read_table2(path):
    table2 = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            number = int(cells[1])
            mainid = cells[0] + ' | ' + f"{number:03d}" + ' | ' + cells[2]
            table2[mainid] = cells[3:]
    return table2


def merge_tables(table1, table2):
    for i in table2:
        tmp = [i] + table1[i] + table2[i]
        tmp = '\t'.join(tmp)
        print(tmp)


if __name__ == '__main__':
    main()
