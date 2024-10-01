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
    parser.add_argument("-s", "--samples", type=str, default=None, required=True,
                          help="Path to file with samples mapped.")
    parser.add_argument("-o", "--out", type=str, default=None, required=True,
                          help="Path to out directory.")
    args = parser.parse_args()

    groups = readSamples(args.samples)
    genes = readGeneList(args.genes)
    exp, samples = readExp(args.EXP, genes)
    final_groups = checkGroups(samples, groups)
    for i in exp:
        x, traces = prepareData(exp[i], final_groups)
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


def readSamples(path):
    groups = {}
    tmp = {2: 'Primary', 3: 'Organoide', 4: 'Xeno'}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            if not line[0:5] == 'BB-ID':
                cells = line.rstrip('\n').split('\t')
                groups[cells[0]] = {}
                for i in range(2, min(len(cells), 5)):
                    groups[cells[0]][tmp[i]] = cells[i]
    infile.close()
    return groups


def readExp(path, genes):
    exp = {}
    s = {}
    slist = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if cells[0] == 'geneNames':
                for i in range(3, len(cells)):
                    s[i] = cells[i]
                    slist.append(cells[i])
            elif cells[0] in genes:
                if not cells[0] in exp:
                    exp[cells[0]] = {}
                exp[cells[0]][cells[2]] = {}
                for i in range(3, len(cells)):
                    exp[cells[0]][cells[2]][s[i]] = float(cells[i])
    return exp, slist


def checkGroups(samples, groups):
    final_groups = {}
    for group in groups:
        if groups[group]['Primary'] in samples or groups[group]['Organoide'] in samples:
            final_groups[group] = {}
            for sample in groups[group]:
                if groups[group][sample] in samples:
                    final_groups[group][sample] = groups[group][sample]
    return final_groups


def prepareData(exp, final_groups):
    tlist = list(exp.keys())
    x = [[], []]
    traces = {}
    for t in tlist:
        traces[t] = []
    for group in final_groups:
        for i in ['Primary', 'Organoide', 'Xeno']:
            if i in final_groups[group]:
                x[0].append(group)
                x[1].append(i)
                for t in tlist:
                    traces[t].append(exp[t][final_groups[group][i]])
    return x, traces


def plotExp(x, traces, outpath, gene):
    fig = go.Figure()
    i = 0
#    for trace in traces:
#        fig.add_bar(x=x, y=traces[trace], name=trace,)
#        fig.update_layout(barmode='stack', yaxis_title='Normalized Counts')
#        i += 1
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
