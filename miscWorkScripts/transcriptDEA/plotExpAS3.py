#!/bin/env python

import argparse
import plotly.graph_objects as go
import plotly.express as px


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-e", "--EXP", type=str, default=None, required=True,
                          help="expression File")
    parser.add_argument("-g", "--genes", type=str, default=None, required=True,
                          help="List of genes in a text file.")
    parser.add_argument("-m", "--mapping", type=str, default=None, required=True,
                          help="TSV Table with sample id (0), subgroup (1) and group (2).")
    parser.add_argument("-o", "--out", type=str, default=None, required=True,
                          help="Path to out directory.")
    args = parser.parse_args()

    genes = readGeneList(args.genes)
    mapping = readMap(args.mapping)
    exp = readExp(args.EXP, genes)
    for i in exp:
        x, traces = prepareData(exp[i], mapping)
        plotExp(x, traces, args.out, i)
        genes.remove(i)
    if genes:
        print('Missing:')
        for i in genes:
            print(i)

def readGeneList(path):
    genes = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            genes.append(line.rstrip('\n'))
    return genes


def readExp(path, genes):
    exp = {}
    s = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if cells[0] == 'gene_name':
                for i in range(3, len(cells)):
                    s[i] = cells[i]
            elif cells[0] in genes:
                if not cells[0] in exp:
                    exp[cells[0]] = {}
                exp[cells[0]][cells[2]] = {}
                for i in range(3, len(cells)):
                    exp[cells[0]][cells[2]][s[i]] = float(cells[i])
    infile.close()
    return exp


def readMap(path):
    mapping = {}
    with open(path, 'r') as infile:
        line = infile.readline()
        line = infile.readline()
        while line:
            cells = line.rstrip('\n').split('\t')
            mapping[cells[0]] = [cells[2], cells[1]]
            line = infile.readline()
    infile.close()
    return mapping


def prepareData(exp, mapping):
    tlist = list(exp.keys())
    x = [[], []]
    traces = {}
    for t in tlist:
        traces[t] = []
    for sample in mapping:
        x[0].append(mapping[sample][0])
        x[1].append(mapping[sample][1])
        for t in tlist:
            traces[t].append(exp[t][sample])
    return x, traces


def plotExp(x, traces, outpath, gene):
    fig = go.Figure()
    i = 0
    for trace in traces:
        fig.add_bar(x=x, y=traces[trace], name=trace,  marker=dict(color=px.colors.qualitative.Light24[i]))
        fig.update_layout(barmode='stack', yaxis_title='Counts [TPM]')
        i += 1
        i = i%24
    fig.update_xaxes(tickangle=90)
    fig.update_layout(
        showlegend=True,
        title={
            'text': gene,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.write_html(outpath + '/' + gene + '.html')
    fig.write_image(outpath + '/' + gene + '.svg', width=4000, height=1000)

if __name__ == '__main__':
    main()
