#!/bin/env python

import argparse
import plotly.express as px
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Get all entries in column x that reach threshold t in column y")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="input table in csv format")
    parser.add_argument("-g", "--groups", type=str, default=None, required=True,
                          help="input table in csv format")
    args = parser.parse_args()

    groups = read_groups(args.groups)
    data = read_infile(args.infile, groups)
    plotbar(data)



def read_groups(path):
    with open(path, 'r') as infile:
        lines = infile.readlines()
        groups = {}
        for line in lines[1:]:
            cells = line.rstrip('\n').split(',')
            groups[cells[0].strip('"')] = cells[1].strip('"')
    return groups


def read_infile(path, groups):
    with open(path, 'r') as infile:
        lines = infile.readlines()
        cells = lines[0].rstrip('\n').split(',')
        x = []
        y = []
        c = []
        tmp = {}
        for i in range(1, len(cells)):
            if cells[i] in groups:
                tmp[i] = groups[cells[i]]
        for line in lines[1:]:
            cells = line.rstrip('\n').split(',')
            for s in tmp:
                x.append(tmp[s])
                y.append(float(cells[s]))
                c.append(cells[0])
    return pd.DataFrame({'Cluster': x, 'Cells [Log2]': y, 'Cell': c})


def plotbar(df):
    fig = px.box(df, x='Cluster', y='Cells [Log2]', color='Cell')
    fig.write_html('Cells_panCK-.html')
    fig.write_image('Cells_panCK-.svg')
    fig.show()


if __name__ == '__main__':
    main()
