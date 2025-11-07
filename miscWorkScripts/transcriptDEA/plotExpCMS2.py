#!/bin/env python

import argparse
import plotly.graph_objects as go
import plotly.express as px


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-e", "--EXP", type=str, default=None, required=True,
                          help="expression File")
    parser.add_argument("-c", "--cms", type=str, default=None, required=True,
                          help="Path to file with cms annotation.")
    parser.add_argument("-g", "--genes", type=str, default=None, required=True,
                          help="List of genes in a text file.")
    args = parser.parse_args()

    cms = readCMS(args.cms)
    exp, samples = readExp(args.EXP)
    genes = readGeneList(args.genes)
    for gene in genes:
        x, y = prepareData(exp, cms, gene)
        plotExp(x, y, gene)


def readGeneList(path):
    genes = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            genes.append(line.rstrip('\n'))
    return genes


def readCMS(path):
    groups = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not (cells[0] == 'Tumor.Sample.ID' or cells[0] == ''):
                groups[cells[0]] = cells[1]
    infile.close()
    return groups


def readExp(path):
    exp = {}
    s = {}
    slist = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if cells[0] == 'gene':
                for i in range(1, len(cells)):
                    s[i] = cells[i]
                    slist.append(cells[i])
            else:
                exp[cells[0]] = {}
                for i in range(1, len(cells)):
                    exp[cells[0]][s[i]] = float(cells[i])
    return exp, slist

def prepareData(exp, cms, gene):
    slist = list(exp[gene].keys())
    x = [[], []]
    y = []
    for sample in slist:
        if not cms[sample] == 'NA':
            y.append(exp[gene][sample])
            x[0].append(cms[sample])
            x[1].append(sample)
    return x, y


def plotExp(x, trace, outname):
    fig = go.Figure()
    fig.add_box(
        x=x[0],
        y=trace,
        name=outname,
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
    )
    fig.update_layout(
        yaxis_title='Normalized Counts',
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
    )
    fig.show()
    fig.write_html(outname + '_box.html')
    fig.write_image(outname + '_box.svg', width=800, height=600)


if __name__ == '__main__':
    main()
