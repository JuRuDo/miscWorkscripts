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
    parser.add_argument("-o", "--outname", type=str, default=None, required=True,
                          help="Outfile name")
    args = parser.parse_args()

    groups = readSamples(args.samples)
    exp, samples = readExp(args.EXP)
    final_groups = checkGroups(samples, groups)
    x, traces = prepareData(exp, final_groups)
    plotExp(x, traces, args.outname)


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


def readExp(path):
    exp = {}
    s = {}
    slist = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
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


def plotExp(x, traces, outname):
    fig = go.Figure()
    i = 0
    for trace in traces:
        fig.add_bar(x=x, y=traces[trace], name=trace,)
        fig.update_layout(yaxis_title='Normalized Counts')
        i += 1
#    i = 0
#    for trace in traces:
#        fig.add_bar(x=x, y=traces[trace], name=trace,  marker=dict(color=px.colors.qualitative.Light24[i]))
#        fig.update_layout(barmode='stack', yaxis_title='Normalized Counts')
#        i += 1
    fig.update_xaxes(tickangle=90)
    fig.show()
    fig.write_html(outname + '.html')
    fig.write_image(outname + '.svg', width=2000, height=1000)


if __name__ == '__main__':
    main()
