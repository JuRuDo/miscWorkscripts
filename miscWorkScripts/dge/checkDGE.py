#!/bin/env python

#######################################################################
# Copyright (C) 2022 Julian Dosch
#
# This file is part of .
#
#  SpICE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SpICE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with expNet.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################



import argparse
from pkg_resources import get_distribution


def read_genelist(path):
    genes = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            genes.append(line.rstrip('\n').lower())
    infile.close()
    return genes

def read_dge(path, genes):
    results = {}
    with open(path, 'r') as infile:
        line = infile.readline()
        line = infile.readline()
        while line:
            cells = line.rstrip('\n').split('\t')
            clusters = int(len(cells) / 5)
            for i in range(clusters):
                if not i in results:
                    results[i] = {'up': [], 'down': []}
                if cells[i*5].lower() in genes:
                    if float(cells[i*5+2]) >= 2.0 and float(cells[i*5+4]) <= 0.05:
                        results[i]['up'].append(cells[i*5])
                    elif float(cells[i*5+2]) <= -2.0 and float(cells[i*5+4]) <= 0.05:
                        results[i]['down'].append(cells[i*5])
            line = infile.readline()
    return results


def write_output(path, results, genes):
    with open(path, 'w') as out:
        tmp = ''
        for i in results:
            tmp = tmp + str(i) + '_up\t' + str(i) + '_down\t'
        tmp = tmp.rstrip('\t') + '\n'
        out.write(tmp)
        tmp = ''
        for x in range(len(genes)):
            for i in results:
                if x < len(results[i]['up']):
                    tmp = tmp + results[i]['up'][x]
                tmp = tmp + '\t'
                if x < len(results[i]['down']):
                    tmp = tmp + results[i]['down'][x]
                tmp = tmp + '\t'
            tmp = tmp.rstrip('\t') + '\n'
            out.write(tmp)
            tmp = ''
    out.close()


def main():
    version = get_distribution('workScripts').version
    parser = argparse.ArgumentParser(description='checks a list of genes for DGE in a file with multiple clusters',
                                     epilog="")
    required = parser.add_argument_group('required arguments')
    parser.add_argument('--version', action='version', version=str(version))
    required.add_argument("-d", "--dge", default=None, type=str, required=True,
                          help="path to the DGE results")
    required.add_argument("-o", "--outpath", default=None, type=str, required=True,
                          help="path to output file")
    required.add_argument("-l", "--genelist", default=None, type=str, required=True,
                          help="path to gene list")
    args = parser.parse_args()

    genes = read_genelist(args.genelist)
    results = read_dge(args.dge, genes)
    write_output(args.outpath, results, genes)


if __name__ == '__main__':
    main()
