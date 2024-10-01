#!/bin/env python

import argparse
import plotly.express as px
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Get all entries in column x that reach threshold t in column y")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="input table in csv format")
    args = parser.parse_args()

    data = read_infile(args.infile)
    name = '.'.join(args.infile.split('/')[-1].split('.')[0:-1])
    plotbar(data, 'cluster', 'sample', name + '_c')
    plotbar(data, 'sample', 'cluster', name + '_s')


def read_infile(path):
    with open(path, 'r') as infile:
        lines = infile.readlines()
        cells = lines[0].rstrip('\n').split(',')
        x = []
        data = {'cluster': [], 'sample': [], 'cells': []}
        for cell in cells[1:]:
            x.append(cell.strip('"'))
        for line in lines[1:]:
            cells = line.rstrip('\n').split(',')
            for i in range(1, len(cells)):
                data['cluster'].append(x[i-1])
                data['sample'].append(cells[0].strip('"'))
                data['cells'].append(int(cells[i].strip('"')))
    return pd.DataFrame(data)


def plotbar(data, x, c, outpath):
    print(data)
    fig = px.bar(data, x=x, y='cells', color=c, color_discrete_sequence=px.colors.qualitative.Light24)
    fig.update_layout(
        barmode='stack'
    )
    fig.write_html(outpath + '.html')
    fig.write_image(outpath + '.png')
    fig.show()
