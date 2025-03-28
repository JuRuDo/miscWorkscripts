#!/bin/env python

#######################################################################
# Copyright (C) 2022 Julian Dosch
#
# This file is part of .
#
#   is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#   is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with expNet.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################


import argparse



def main():
    parser = argparse.ArgumentParser(description="create line plot that shows which regions of a sequence have ")
    parser.add_argument("-d", "--dge", type=str, default=None, required=True,
                          help="DGE file")
    parser.add_argument("-o", "--out", type=str, default=None, required=True,
                          help="output file")
    parser.add_argument("-g", "--genes", type=str, default=None, required=True,
                          help="gene position table, needs geneID [0] and start [1], ordered by start")
    parser.add_argument("-l", "--regions", type=str, default=None, required=True,
                          help="table of regions of interest with start [0] and stop [1]")
    parser.add_argument("-r", "--reg", type=str, default="a",
                          help="take all [a], only upregulated [+], or only downregulated [-]")
    args = parser.parse_args()

    if args.reg == "+":
        mode = 1
    elif args.reg == "-":
        mode = 2
    elif args.reg == "a":
        mode = 0
    else:
        print("unknown --reg option, continuing with 'a'")
        mode = 0
    genes = readChr(args.genes)
    dge = readDGE(args.dge, mode)
    areas = readAreas(args.regions)
    with open(args.out, 'w') as out:
        for area in areas:
            deGenes = assessRegion(area, genes, dge)
            out.write(str(area[0]) + '-' + str(area[1]) + '\t' + '\t'.join(deGenes) + '\n')
    out.close()


def readAreas(path):
    areas = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            areas.append((int(cells[0]), int(cells[1])))
    infile.close()
    return areas


def readChr(path):
    genes =  []
    first = None
    last = 0
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if not first:
                first = int(cells[1])
            if int(cells[1]) > last:
                last = int(cells[1])
            genes.append((int(cells[1]), cells[0]))
    infile.close()
    return genes


def readDGE(path, mode):
    dge = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[0].strip('"') == 'gene':
                if cells[3] == "NA":
                    dge[cells[0].strip('"')] = False
                else:
                    if mode == 1:
                        dge[cells[0].strip('"')] = float(cells[3]) <= 0.05 and float(cells[2]) > 0.5
                    elif mode == 2:
                        dge[cells[0].strip('"')] = float(cells[3]) <= 0.05 and float(cells[2]) < -0.5
                    else:
                        dge[cells[0].strip('"')] = float(cells[3]) <= 0.05
    infile.close()
    return dge


def assessRegion(area, genes, dge):
    deGenes = []
    for i in genes:
        if i[0] >= area[0] and i[0] <= area[1]:
            if i[1] in dge:
                if dge[i[1]]:
                    deGenes.append(i[1])
    return deGenes


if __name__ == '__main__':
    main()
