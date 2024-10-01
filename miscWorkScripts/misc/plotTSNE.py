#!/bin/env python

import argparse
import plotly.express as px
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Get all entries in column x that reach threshold t in column y")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="input table in csv format")
    parser.add_argument("-m", "--map", type=str, default=None, required=True,
                          help="input table in csv format")
    parser.add_argument("-c", "--color", type=str, default='Leiden',
                          help="Color pojnts by either Leiden, Lovain, or Batch")
    parser.add_argument("-o", "--out", type=str, default='Leiden.html',
                          help="output file")
    args = parser.parse_args()

    TSNEdata, c1, c2 = read_infile(args.infile)
    TSNEdata = read_map(args.map, TSNEdata, args.color)
    plotTSNE(TSNEdata, c1, c2, args.out, args.color)


def read_infile(path):
    TSNEdata = {}
    with open(path, 'r') as infile:
        line = infile.readline()
        cells = line.rstrip('\n').split(',')
        c1 = cells[1].strip('"')
        c2 = cells[2].strip('"')
        TSNEdata[c1] = []
        TSNEdata[c2] = []
        line = infile.readline()
        while line:
            cells = line.rstrip('\n').split(',')
            TSNEdata[c1].append(float(cells[1].strip('"')))
            TSNEdata[c2].append(float(cells[2].strip('"')))
            line = infile.readline()
    infile.close()
    return TSNEdata, c1, c2


def read_map(path, TSNEdata, method):
    c = 'Cluster'
    if method == 'Batch':
        c = 'Batch'
    TSNEdata[c] = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[1].strip('"') == 'Batch':
                if method == 'Batch':
                    TSNEdata['Batch'].append(cells[1].strip('"'))
                elif method == 'Lovain':
                    TSNEdata['Cluster'].append(cells[2].strip('"'))
                else:
                    TSNEdata['Cluster'].append(cells[3].strip('"'))
    infile.close()
    return TSNEdata


def plotTSNE(TSNEdata, c1, c2, outpath, method):
    c = 'Cluster'
    if method == 'Batch':
        c = 'Batch'
    df = pd.DataFrame(TSNEdata)
    fig1 = px.scatter(df, x=c1, y=c2, color=c, color_discrete_sequence=px.colors.qualitative.Light24)
    fig1.update_layout(font=dict(size=14), legend={'itemsizing': 'constant'})
    fig1.show()
    fig1.write_html(outpath)


if __name__ == '__main__':
    main()
