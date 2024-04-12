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
    args = parser.parse_args()

    TSNEdata = read_infile(args.infile)
    TSNEdata = read_map(args.map, TSNEdata)
    plotTSNE(TSNEdata)


def read_infile(path):
    TSNEdata = {'TSNE1': [], 'TSNE2': [], 'Batch':[]}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[1] == 'TSNE1':
                TSNEdata['TSNE1'].append(float(cells[1]))
                TSNEdata['TSNE2'].append(float(cells[2]))
    infile.close()
    return TSNEdata


def read_map(path, TSNEdata):
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[1] == 'x':
                TSNEdata['Batch'].append(cells[1])
    infile.close()
    return TSNEdata


def plotTSNE(TSNEdata):
    df = pd.DataFrame(TSNEdata)
    fig1 = px.scatter(df, x="TSNE1", y="TSNE2", color='Batch', color_discrete_sequence=px.colors.qualitative.Light24)
    fig1.update_layout(font=dict(size=14), legend={'itemsizing': 'constant'})
    fig1.show()
    fig1.write_html('TSNE.html')


if __name__ == '__main__':
    main()
