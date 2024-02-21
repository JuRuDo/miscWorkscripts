#!/bin/env python

import argparse
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Combine individual expression tables of samples with output of DEA")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input csv table, first columns should be geneNames, geneIDs and transcriptIDs")
    parser.add_argument("-c", "--FPKMcutoff", type=float, default=1.0,
                          help="FPKM cutoff.")
    parser.add_argument("-s", "--samples", type=str, default=None, required=True,
                          help="Path to file with samples mapped to condition.")
    parser.add_argument("-p", "--sampleCutoff", type=float, default=0.0,
                          help="Percentage of samples in a condition a transcript must be expressed in.")
    parser.add_argument("-o", "--output", type=str, default='.',
                          help="output folder")
    args = parser.parse_args()

    name = '.'.join(args.input.split('/')[-1].split('.')[0:-1])
    sdict = readSamples(args.samples)
    genedict, conditions = readInfile(args.input, sdict, args.FPKMcutoff, args.sampleCutoff)
    normalized, pairs, genedict = normalizegenedict(genedict, conditions)
    writeNormalized(normalized, args.output, name, conditions, args.FPKMcutoff, args.sampleCutoff)
    plotAS(genedict, conditions, name, args.output, args.FPKMcutoff, args.sampleCutoff)


def readSamples(path):
    sdict = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[0] == 'ids':
                sdict[cells[0]] = cells[1]
    infile.close()
    return sdict

def readInfile(path, sdict, fpkm, percS):
    genedict = {}
    samples = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if cells[0].strip('"') == 'geneNames':
                for i in range(6, len(cells)):
                    if not sdict[cells[i].strip('"')[5:]] in samples:
                        samples[sdict[cells[i].strip('"')[5:]]] = []
                    samples[sdict[cells[i].strip('"')[5:]]].append(i)
            else:
                if not cells[1].strip('"') in genedict:
                    genedict[cells[1].strip('"')] = {}
                    for condition in samples:
                        genedict[cells[1].strip('"')][condition] = 0
                for condition in samples:
                    tmp = 0
                    for sample in samples[condition]:
                        if float(cells[sample].strip('"')) >= fpkm:
                            tmp += 1
                    if 0.0 < tmp / len(samples[condition]) >= percS:
                        genedict[cells[1].strip('"')][condition] += 1
    infile.close()
    return genedict, list(samples.keys())


def normalizegenedict(genedict, conditions):
    normalized = {}
    pairs = {}
    for i in range(len(conditions)):
        if i < len(conditions) - 1:
            for x in range(i+1, len(conditions)):
                pairs[(conditions[i], conditions[x])] = [0, 0]
    for gene in genedict:
        maxe = 0.0
        normalized[gene] = {}
        for condition in conditions:
            if genedict[gene][condition] > maxe:
                maxe = genedict[gene][condition]
            normalized[gene][condition] = genedict[gene][condition]
        if not maxe == 0.0:
            for condition in conditions:
                normalized[gene][condition] = genedict[gene][condition] / maxe
        for pair in pairs:
            if normalized[gene][pair[0]] > 0 and normalized[gene][pair[1]] > 0:
                if normalized[gene][pair[0]] > normalized[gene][pair[1]]:
                    pairs[pair][0] += 1
                elif normalized[gene][pair[0]] < normalized[gene][pair[1]]:
                    pairs[pair][1] += 1
        for condition in conditions:
            genedict[gene][condition] = str(genedict[gene][condition])
    for pair in pairs:
        print(pair[0] + '/' + pair[1] + ': ' + str(pairs[pair][0]) + '/' + str(pairs[pair][1]))
    return normalized, pairs, genedict


def plotAS(genedict, conditions, name, path, fpkm, cutoff):
    df = pd.DataFrame(genedict).T
    bins = []
    for condition in conditions:
        bins.extend(list(pd.unique(df[condition])))
    bins = sorted(set(bins), key=int)
    fig = make_subplots(rows=3, cols=1)
    colors = ['blue', 'red', 'green', 'yellow', 'purple']
    for i in range(len(conditions)):
        fig = fig.add_trace(go.Histogram(x=df[df[conditions[i]].isin(bins[0:2])][conditions[i]], name=conditions[i],
                            marker=dict(color=colors[i])))
    for i in range(len(conditions)):
        fig = fig.add_trace(go.Histogram(x=df[df[conditions[i]].isin(bins[3:11])][conditions[i]], name=conditions[i],
                                         marker=dict(color=colors[i]), showlegend=False), row=2, col=1)
    for i in range(len(conditions)):
        fig = fig.add_trace(go.Histogram(x=df[df[conditions[i]].isin(bins[11:])][conditions[i]], name=conditions[i],
                                         marker=dict(color=colors[i]), showlegend=False), row=3, col=1)
    fig.update_xaxes(categoryorder='array',
                     categoryarray=bins)
    fig.show()
    fig.write_image(path + "/" + name + '_FPKM' + str(fpkm) + '_c' + str(cutoff) + ".svg")


def writeNormalized(normalized, path, name, conditions, fpkm, cutoff):
    with open(path + '/' + name + '_AS_events_FPKM' + str(fpkm) + '_c' + str(cutoff) + '.tsv', 'w') as out:
        tmp = 'geneID'
        for condition in conditions:
            tmp = tmp + '\t' + condition
        out.write(tmp + '\n')
        for gene in normalized:
            tmp = gene
            for condition in conditions:
                tmp = tmp + '\t' + str(normalized[gene][condition])
            out.write(tmp + '\n')
    out.close()


if __name__ == '__main__':
    main()
