#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Pair replicate samples from SRA_RunTable")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                        help="input table in csv format")
    args = parser.parse_args()

    outdict = readInfile(args.input)
    writeOutfile(outdict)


def readInfile(path):
    outdict = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            if not line[0:3] == "Run":
                cells = line.rstrip('\n').split(',')
                if cells[1] not in outdict:
                    outdict[cells[1]] = []
                outdict[cells[1]].append(cells[0])
    infile.close()
    return outdict


def writeOutfile(outdict):
    print("Patient\tR1\tR2")
    for patient in outdict:
        print(patient + '\t' + outdict[patient][0] + '\t' + outdict[patient][1])


if __name__ == '__main__':
    main()
