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
    parser.add_argument("-p", "--pairs", type=str, default=None, required=True,
                          help="TSV Table with patient id (0), sample 1 (1) and sample 2 (2).")
    parser.add_argument("-o", "--out", type=str, default=None, required=True,
                          help="Path to out directory.")
    args = parser.parse_args()

    genes = readGeneList(args.genes)
    pairs, patients = readPairs(args.pairs)
    exp = readExp(args.EXP, genes, pairs)
    for i in exp:
        x, traces = prepareData(exp[i], patients)
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


def readExp(path, genes, pairs):
    exp = {}
    s = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if cells[0] == 'geneNames':
                for i in range(3, len(cells)):
                    s[i] = cells[i]
            elif cells[0] in genes:
                if not cells[0] in exp:
                    exp[cells[0]] = {}
                exp[cells[0]][cells[2]] = {}
                for i in range(3, len(cells)):
                    if pairs[s[i]] not in exp[cells[0]][cells[2]]:
                        exp[cells[0]][cells[2]][pairs[s[i]]] = 0.0
                    exp[cells[0]][cells[2]][pairs[s[i]]] += float(cells[i])
                for i in exp[cells[0]][cells[2]]:
                    exp[cells[0]][cells[2]][i] = exp[cells[0]][cells[2]][i]/2.0
    infile.close()
    return exp


def prepareData(exp, samples):
    tlist = list(exp.keys())
    x = []
    traces = {}
    for t in tlist:
        traces[t] = []
    for sample in samples:
            x.append(sample)
            for t in tlist:
                traces[t].append(exp[t][sample])
    return x, traces


def readPairs(path):
    pairs = {}
    patients = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if not cells[0] == 'Patient':
                pairs[cells[1]] = cells[0]
                pairs[cells[2]] = cells[0]
                patients.append(cells[0])
    infile.close()
    return pairs, patients


def plotExp(x, traces, outpath, gene):
    fig = go.Figure()
    i = 0
    for trace in traces:
        fig.add_bar(x=x, y=traces[trace], name=trace,  marker=dict(color=px.colors.qualitative.Light24[i]))
        fig.update_layout(barmode='stack', yaxis_title='Normalized Counts')
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
    fig.write_image(outpath + '/' + gene + '.svg', width=2000, height=1000)

if __name__ == '__main__':
    main()
