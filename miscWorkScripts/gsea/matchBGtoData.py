#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Match gene Names in BG file to DEG dataset. Fix case issues in BG file")
    parser.add_argument("-b", "--bg", type=str, default=None, required=True,
                          help="input bg file, should be in .gmt format")
    parser.add_argument("-d", "--dataset", type=str, default=None, required=True,
                          help="Dataset, in .csv format (comma separated), first column should be gene name")
    parser.add_argument("-o", "--output", type=str, default=None,
                          help="output file, will be the bg with fixed case")

    args = parser.parse_args()

    names = read_dataset(args.dataset)
    outpath = '.'.join(args.bg.split('.')[0:-1]) + '_caseChecked.gmt'
    if args.output:
        outpath = args.output
    match_bg(args.bg, outpath, names)


def read_dataset(path):
    names = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.split(',')
            if not cells[0] == 'genes':
                names[cells[0].lower()] = cells[0]
    infile.close()
    return names


def match_bg(bg_in, bg_out, names):
    missing = {}
    infile = open(bg_in, 'r')
    out = open(bg_out, 'w')
    for line in infile.readlines():
        cells = line.rstrip('\n').split('\t')
        new_cells = [cells[0], cells[1]]
        for name in cells[2:]:
            if name.lower().capitalize() in names:
                new_cells.append(names[name.lower().capitalize()])
            else:
                new_cells.append(name.lower().capitalize())
                if not cells[0] in missing:
                    missing[cells[0]] = []
                missing[cells[0]].append(name.lower().capitalize())
        out.write('\t'.join(new_cells) + '\n')
    if missing:
        print('# The following genes could not be found in the dataset:')
        for signature in missing:
            print(signature + ':\t' + ','.join(missing[signature]))
    infile.close()
    out.close()


if __name__ == '__main__':
    main()
