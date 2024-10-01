#!/bin/env python

import argparse


def main():
    parser = argparse.ArgumentParser(description="Use OMA api to download OMA groups by their id")
    parser.add_argument("-i", "--inpath", type=str, default=None, required=True,
                        help="inpath")
    args = parser.parse_args()
    with open(args.inpath, 'r') as infile:
        for line in infile.readlines():
            a = False
            cells = line.rstrip('\n').split(',')
            for i in cells[1:]:
                try:
                    x = float(i)
                except:
                    x = 0.5
                if not x.is_integer():
                    a = True
            if a:
                print(cells[0])


if __name__ == '__main__':
    main()
