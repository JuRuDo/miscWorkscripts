#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Pair healty and tumor samples from SRA_RunTable")
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
                if cells[2] not in outdict:
                    outdict[cells[2]] = {'H': '', 'T': ''}
                if cells[1] == "No":
                    outdict[cells[2]]['H'] = cells[0]
                else:
                    outdict[cells[2]]['T'] = cells[0]
    infile.close()
    return outdict


def writeOutfile(outdict):
    print("Patient\tHealthy\tTumor")
    for patient in outdict:
        print(patient + '\t' + outdict[patient]['H'] + '\t' + outdict[patient]['T'])


if __name__ == '__main__':
    main()
