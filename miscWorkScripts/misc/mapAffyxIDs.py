#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Add gene name to table")
    parser.add_argument("-m", "--mapping", type=str, default=None, required=True,
                        help="input table in tsv format")
    parser.add_argument("-e", "--expression", type=str, default=None, required=True,
                        help="input table in tsv format")
    args = parser.parse_args()

    mapping = read_mapping(args.mapping)
    map_ids(args.expression, mapping)


def read_mapping(path):
    mapping = {}
    final_mapping = {}
    double = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if cells[0] not in mapping:
                mapping[cells[0]] = cells[1]
            else:
                double.append(cells[0])
        for d in mapping:
            if d not in double:
                final_mapping[d] = mapping[d]
    infile.close()
    return final_mapping


def map_ids(path, mapping):
    exp = {}
    out = open(path.rstrip('.csv') + 'mapped.csv', 'w')
    with open(path, 'r') as infile:
        line = infile.readline()
        out.write(line)
        line = infile.readline()
        while line:
            cells = line.rstrip('\n').split('\t')
            if cells[0] in mapping:
                gid = mapping[cells[0]]
                if gid not in exp:
                    exp[gid] = []
                    for i in cells[1:]:
                        exp[gid].append(0.0)
                for i in range(len(cells[1:])):
                    exp[gid][i] += float(cells[i+1])
            line = infile.readline()
    infile.close()
    for i in exp:
        str_elements = [str(element) for element in exp[i]]
        tmp = i + '\t' + '\t'.join(str_elements) + '\n'
        out.write(tmp)
    out.close()


if __name__ == '__main__':
    main()
