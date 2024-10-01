#!/bin/env python

import argparse
import plotly.graph_objects as go



def main():
    parser = argparse.ArgumentParser(description="Plot DE results")
    parser.add_argument("-c", "--cellDE", type=str, default=None, required=True,
                          help="input table in csv format")
    parser.add_argument("-g", "--geneDE", type=str, default=None, required=True,
                          help="input table in csv format")
    args = parser.parse_args()

    x, traces = readCellDE(args.cellDE)
    x, traces = readGeneDE(args.geneDE, x, traces)
    plotDE(x, traces)


def readCellDE(path):
    traces = {'< 0.05': [], '>= 0.05': []}
    x = [[], []]
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[0] == '':
                x[0].append(cells[0].split('.')[0])
                tmp = cells[0].split('.')[1]
                if tmp == 'panCK0':
                    x[1].append('T_cells.panCK-')
                else:
                    x[1].append('T_cells.panCK+')
                if float(cells[5]) < 0.05:
                    traces['< 0.05'].append(float(cells[1]))
                    traces['>= 0.05'].append(0.0)
                else:
                    traces['>= 0.05'].append(float(cells[1]))
                    traces['< 0.05'].append(0.0)
    return x, traces


def readGeneDE(path, x, traces):
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[0] == '':
                x[0].append(cells[0])
                x[1].append('Decorin.Stroma')
                if float(cells[5]) < 0.05:
                    traces['< 0.05'].append(float(cells[1]))
                    traces['>= 0.05'].append(0.0)
                else:
                    traces['>= 0.05'].append(float(cells[1]))
                    traces['< 0.05'].append(0.0)
    return x, traces


def plotDE(x, traces):
    fig = go.Figure()
    i = 0
    for trace in traces:
        fig.add_bar(x=x, y=traces[trace], name=trace, )
        fig.update_layout(barmode='stack', yaxis_title='LogFoldChange')
        i += 1
    #    i = 0
    #    for trace in traces:
    #        fig.add_bar(x=x, y=traces[trace], name=trace,  marker=dict(color=px.colors.qualitative.Light24[i]))
    #        fig.update_layout(barmode='stack', yaxis_title='Normalized Counts')
    #        i += 1
    fig.update_xaxes(tickangle=90)
    fig.show()
    fig.write_html('SpatialDE.html')
    fig.write_image('SpatialDE.svg', width=2000, height=1000)


if __name__ == '__main__':
    main()
