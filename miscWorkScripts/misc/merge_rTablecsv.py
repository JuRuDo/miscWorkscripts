#!/bin/env python

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Get length of all transcripts")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                        help="path to input directory with csv files")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                        help="output file")
    args = parser.parse_args()

    cdata = {}
    for file in os.listdir(args.input):
        if file.endswith(".csv"):
            with open(args.input + '/' + file, "r") as inputFile:
                cdata[file.rstrip(".csv")] = []
                for line in inputFile:
                    cells = line.rstrip("\n").split(",")
                    cdata[file.rstrip(".csv")].append(cells[2].strip('"'))
            inputFile.close()

    with open(args.output, "w") as outputFile:
        for key in cdata.keys():
            outputFile.write(key + "\t" + "\t".join(cdata[key][1:]) + "\n")


if __name__ == '__main__':
    main()
