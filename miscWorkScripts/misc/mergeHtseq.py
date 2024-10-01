#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input folder containing htseq files.")
    parser.add_argument("-s", "--samples", type=str, default=None, required=True,
                          help="Path to file with samples.")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    args = parser.parse_args()

    samples = readSamples(args.samples)

    final = []
    for sample in samples:
        final = readTable(final, args.input + '/htseq_' + sample + '.counts', sample)
    with open(args.output, 'w') as out:
        for x in final:
            out.write('\t'.join(x) + '\n')
    out.close()


def readSamples(path):
    samples = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            samples.append(line.rstrip('\n'))
    infile.close()
    return samples


def readTable(final, path, sample):
    with open(path, 'r') as infile:
        first = False
        if not final:
            first = True
        i = 1
        line = infile.readline()
        if first:
            final.append([''])
        final[0].append(sample)
        while line:
            cells = line.rstrip('\n').split('\t')
            if first:
                final.append([cells[0]])
            final[i].append(cells[1])
            i += 1
            line = infile.readline()
    infile.close()
    return final


if __name__ == '__main__':
    main()
