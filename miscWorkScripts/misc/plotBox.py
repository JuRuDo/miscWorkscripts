#!/bin/env python

import argparse
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def main():
    parser = argparse.ArgumentParser(description="Get all entries in column x that reach threshold t in column y")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                          help="input table in csv format")
    parser.add_argument("-g", "--groups", type=str, default=None, required=True,
                          help="input table in csv format")
    parser.add_argument("--gene", type=str, default='DCN',
                          help="input table in csv format")
    args = parser.parse_args()

    groups = read_groups(args.groups)
    data = read_infile(args.infile, groups, args.gene)
    name = '.'.join(args.infile.split('/')[-1].split('.')[0:-1])
    plotbar(data, name + '_' + args.gene)



def read_groups(path):
    with open(path, 'r') as infile:
        lines = infile.readlines()
        groups = {}
        for line in lines[1:]:
            cells = line.rstrip('\n').split(',')
            groups[cells[0].strip('"')] = cells[2].strip('"')
    return groups


def read_infile(path, groups, gene):
    with open(path, 'r') as infile:
        lines = infile.readlines()
        cells = lines[0].rstrip('\n').split(',')
        x = []
        traces = {}
        for cell in cells[1:]:
            x.append(cell.strip('"'))
        for line in lines[1:]:
            cells = line.rstrip('\n').split(',')
            if cells[0].strip('"') == gene:
                for i in range(1, len(cells)):
                    if not groups[x[i-1]] in traces:
                        traces[groups[x[i-1]]] = []
                    traces[groups[x[i - 1]]].append(float(cells[i].strip('"')))
    return traces


def plotbar(traces, outpath):
    fig = go.Figure()
    max_val = 0
    for trace in ['Tumor.panCK-', 'IM.panCK-', 'Stroma.panCK-']:
#    for trace in ['Tumor.panCK-', 'Tumor.panCK+', 'IM.panCK-', 'IM.panCK+', 'Stroma.panCK-']:
        fig.add_trace(go.Box(
            y=traces[trace],
            name=trace,
            jitter=0.3,
            pointpos=-1.8,
            marker=dict(
                color='White',
                size=5,
                line=dict(
                    color='Black',
                    width=1
                )
            ),
            boxpoints='all',
            line_color='Black',
            line_width=1,
            fillcolor='White',
            showlegend=False
        ))
        if max(traces[trace]) > max_val:
            max_val = max(traces[trace])
    fig.update_layout(
        plot_bgcolor='white',
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        gridcolor='lightgrey',
        title='log counts'
    )
    fig.write_html(outpath + '.html')
    fig.write_image(outpath + '.png')
    fig.write_image(outpath + '.svg')
    fig.show()

if __name__ == '__main__':
    main()
