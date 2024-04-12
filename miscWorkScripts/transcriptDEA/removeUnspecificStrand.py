#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Removes transcripts with unspecific strand from file")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                        help="input table")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="output file")
    args = parser.parse_args()

    if args.output:
        outpath = args.output
    else:
        outpath = '.'.join(args.input.split('.')[0:-1]) + '_noUnspecific.gtf'
    removeUnspec(args.input, outpath)


def removeUnspec(inpath, outpath):
    out = open(outpath, 'w')
    infile = open(inpath, 'r')
    countT = 0
    countE = 0
    for line in infile.readlines():
        if line[0] == '#' or not line.split('\t')[6] == '.':
            cells = line.rstrip('\n').split('\t')
            lastcells = cells[-1].split(';')
            if lastcells[-1][1:12] == 'ref_gene_id':
                gid = lastcells[-1].split(' ')[2].strip('"')
                print(gid)
                newline = '\t'.join(cells[0:-1]) + '\tgene_id "' + gid + '";' + ';'.join(lastcells[1:]) + '\n'
                out.write(newline)
            else:
                out.write(line)
        elif line.split('\t')[2] == 'transcript':
            countT += 1
        elif line.split()[2] == 'exon':
            countE += 1
        else:
            print(line)
    infile.close()
    out.close()
    print('Removed ' + str(countT) + ' transcripts with ' + str(countE) + ' exons')


if __name__ == '__main__':
    main()
