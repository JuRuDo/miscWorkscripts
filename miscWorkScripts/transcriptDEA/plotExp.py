#!/bin/env python

import argparse
import plotly.graph_objects as go


def main():
    parser = argparse.ArgumentParser(description="Combine individual expression tables of samples with output of DEA")
    parser.add_argument("-e", "--EXP", type=str, default=None, required=True,
                          help="expression File")
    parser.add_argument("-s", "--samples", type=str, default=None, required=True,
                          help="Path to file with samples mapped.")
    args = parser.parse_args()

    groups = readSamples(args.samples)
    exp, samples = readExp(args.EXP)
    final_groups = checkGroups(samples, groups)
    x, traces = prepareData(exp, final_groups)
    plotExp(x, traces)


def readSamples(path):
    groups = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            if not line[0:5] == 'BB-ID':
                cells = line.rstrip('\n').split('\t')
                groups[cells[0]] = []
                for i in range(2,len(cells)):
                    groups[cells[0]].append(cells[i])
    infile.close()
    return groups


def readExp(path):
    exp = {}
    s = {}
    slist = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if cells[0] == '':
                for i in range(1, len(cells)):
                    s[i] = cells[i]
                    slist.append(cells[i])
            else:
                exp[cells[0]] = {}
                for i in range(1, len(cells)):
                    exp[cells[0]][s[i]] = float(cells[i])
    return exp, slist


def checkGroups(samples, groups):
    final_groups = {}
    for group in groups:
        if groups[group][0] in samples:
            final_groups[group] = [groups[group][0]]
            for sample in groups[group][1:]:
                if sample in samples:
                    final_groups[group].append(sample)
    return final_groups


def prepareData(exp, final_groups):
    tlist = list(exp.keys())
    x = [[], []]
    traces = {}
    for t in tlist:
        traces[t] = []
    tmp = {0: 'Tumor', 1: 'Organoide', 2: 'Xeno'}
    for group in final_groups:
        for i in range(len(final_groups[group])):
            x[0].append(group)
            x[1].append(tmp[i])
            for t in tlist:
                traces[t].append(exp[t][final_groups[group][i]])
    return x, traces


def plotExp(x, traces):
    fig = go.Figure()
    for trace in traces:
        fig.add_bar(x=x, y=traces[trace], name=trace)
        fig.update_layout(barmode='stack', yaxis_title='FPKM')
    fig.show()
    fig.write_html('EXP.html')
    fig.write_image('EXP.svg', width=1600, height=1000)


if __name__ == '__main__':
    main()
