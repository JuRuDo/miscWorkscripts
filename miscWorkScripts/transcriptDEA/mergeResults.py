#!/bin/env python

import argparse

def main():
    parser = argparse.ArgumentParser(description="Combine individual expression tables of samples with output of DEA")
    parser.add_argument("-s", "--samples", type=str, default=None, required=True,
                          help="a list file contatining  the location of all individual tsv expression tables of samples")
    parser.add_argument("-d", "--dea", type=str, default='.',
                          help="DEA table")
    parser.add_argument("-o", "--output", type=str, default='.',
                          help="output file")
    args = parser.parse_args()
    print('Merging...')
    samples = readSamples(args.samples)
    expdict = {}
    for sample in samples:
        expdict = readEXP(sample, expdict)
    mergeDEA(args.dea, expdict, args.output)
    print('done!')

def readEXP(path, expdict):
    sample = '.'.join(path.split('/')[-1].split('.')[0:-1])
    expdict[sample] = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            if not line[0] == '#':
                cells = line.rstrip('\n').split()
                expdict[sample][cells[1]] = cells[2] + '/' + cells[3]
    infile.close()
    return expdict

def readSamples(path):
    samples = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            samples.append(line.rstrip('\n'))
    infile.close()
    return samples

def mergeDEA(path, expdict, outpath):
    out = open(outpath, 'w')
    samples = list(expdict.keys())
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            tmp = ','.join(cells)
            if cells[0] == '"geneNames"':
                for sample in samples:
                    tmp = tmp + ',"' + sample + ' [FPKM/TPM]"'
                out.write(tmp + '\n')
            else:
                if not cells[4] == 'NA':
                    for sample in samples:
                        tmp = tmp + ',' + expdict[sample][cells[2].strip('"')] + ''
                    out.write(tmp + '\n')
    out.close()
    infile.close()

if __name__ == '__main__':
    main()