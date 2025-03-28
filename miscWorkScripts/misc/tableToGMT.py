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


def main():
    parser = argparse.ArgumentParser(description="create gmt file out of two column table (gene, signature)")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="base input table in csv format")
    parser.add_argument("-o", "--out", type=str, default='out.gmt',
                          help="output file")
    args = parser.parse_args()

    signatures = read_infile(args.infile)
    write_gmt(args.out, signatures)



def read_infile(path):
    signatures = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if cells[1] not in signatures:
                signatures[cells[1]] = []
            signatures[cells[1]].append(cells[0])
    infile.close()
    return signatures


def write_gmt(path, signatures):
    with open(path, 'w') as out:
        for sig in signatures:
            out.write(sig + '\tNA\t' + '\t'.join(signatures[sig]) + '\n')
    out.close()