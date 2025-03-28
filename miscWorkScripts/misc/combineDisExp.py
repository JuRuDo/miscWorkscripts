#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Merge multiple expression table with no headers")
    parser.add_argument("-l", "--list", type=str, default=None, required=True,
                        help="list of input tables in tsv format")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                        help="output table in tsv format")
    args = parser.parse_args()

    pathlist = read_file_list(args.list)
    table = {}
    for infile in pathlist:
        table = read_table(infile, table)
    genes = list(table.keys())
    cut = len(pathlist)
    print(table)
    for gene in genes:
        if len(table[gene]) < cut:
            del table[gene]
    with open(args.output, 'w') as out:
        for entry in pathlist:
            out.write('\t' + pathlist[entry])
        out.write('\n')
        for gene in table:
            out.write(gene + '\t' + '\t'.join(table[gene]) + '\n')
    out.close()


def read_file_list(path):
    pathlist = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            pathlist[cells[0]] = cells[1]
    infile.close()
    return pathlist


def read_table(path, table):
    with open(path, 'r') as infile:
        if not table:
            for line in infile.readlines():
                cells = line.rstrip('\n').split('\t')
                table[cells[0].split('.')[0]] = [cells[1]]
        else:
            for line in infile.readlines():
                cells = line.rstrip('\n').split('\t')
                if cells[0].split('.')[0] in table:
                    table[cells[0].split('.')[0]].append(cells[1])
    infile.close()
    return table


if __name__ == '__main__':
    main()
