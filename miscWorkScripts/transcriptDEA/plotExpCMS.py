#!/bin/env python

import argparse
import plotly.graph_objects as go
import plotly.express as px


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-e", "--EXP", type=str, default=None, required=True,
                          help="expression File")
    parser.add_argument("-s", "--samples", type=str, default=None, required=True,
                          help="Path to file with samples mapped.")
    parser.add_argument("-c", "--cms", type=str, default=None, required=True,
                          help="Path to file with cms annotation.")
    parser.add_argument("-g", "--genes", type=str, default=None, required=True,
                          help="List of genes in a text file.")
    args = parser.parse_args()

    groups = readSamples(args.samples)
    cms = readCMS(args.cms)
    exp, samples = readExp(args.EXP)
    genes = readGeneList(args.genes)
    for gene in genes:
        x, y = prepareData(exp, groups, cms, gene)
        plotExp(x, y, gene)


def readGeneList(path):
    genes = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            genes.append(line.rstrip('\n'))
    return genes


def readSamples(path):
    groups = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            if not line[0:5] == 'BB-ID':
                cells = line.rstrip('\n').split('\t')
                for i in range(2,6):
                    if cells[i]:
                        groups[cells[i]] = cells[0]
    infile.close()
    return groups


def readCMS(path):
    groups = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[0] == 'id':
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

def prepareData(exp, groups, cms, gene):
    slist = list(exp[gene].keys())
    x = [[], []]
    y = []
    for sample in slist:
        y.append(exp[gene][sample])
        x[0].append(cms[sample])
        x[1].append(groups[sample])
    return x, y


def plotExp(x, trace, outname):
    fig = go.Figure()
    fig.add_bar(x=x, y=trace, name=outname)
    fig.update_layout(yaxis_title='Normalized Counts')
    fig.update_xaxes(tickangle=90)
    fig.show()
    fig.write_html(outname + '.html')
    fig.write_image(outname + '.svg', width=2000, height=1000)
    fig = go.Figure()
    fig.add_box(x=x[0], y=trace, name=outname)
    fig.update_layout(yaxis_title='Normalized Counts')
    fig.show()
    fig.write_html(outname + '_box.html')
    fig.write_image(outname + '_box.svg', width=2000, height=1000)


if __name__ == '__main__':
    main()
