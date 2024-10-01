#!/bin/env python


import plotly.graph_objects as go
import argparse



def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-e", "--expression", type=str, default=None, required=True,
                          help="Table containing the transcript expression.")
    parser.add_argument("-t", "--tags", type=str, default=None, required=True,
                          help="Table containing the transcript annotation.")
    parser.add_argument("-s", "--samples", type=str, default=None, required=True,
                          help="Sample information.")
    args = parser.parse_args()

    tdict = read_flags(args.tags)
    per, samples = read_exp(args.expression, tdict)
    groups = readSamples(args.samples)
    final_groups = checkGroups(samples, groups)
    counts = count_genes(per, tdict)
    x, traces, alttrace = prepareData(counts, final_groups)
    plotExp(x, traces, alttrace)


def read_flags(path):
    tdict = {}
    with open(path, 'r') as infile:
        line = infile.readline()
        cells = line.rstrip('\n').split(',')
        for i in range(len(cells)):
            if cells[i] == 'tag':
                i_tag = i
            if cells[i] == 'transcript_id':
                i_transcript = i
            if cells[i] == 'gene_id':
                i_gene = i
        line = infile.readline()
        while line:
            cells = line.rstrip('\n').split(',')
            tdict[cells[i_transcript]] = (cells[i_gene], cells[i_tag])
            line = infile.readline()
    infile.close()
    return tdict


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


def checkGroups(samples, groups):
    final_groups = {}
    for group in groups:
        if groups[group]['Primary'] in samples or groups[group]['Organoide'] in samples:
            final_groups[group] = {}
            for sample in groups[group]:
                if groups[group][sample] in samples:
                    final_groups[group][sample] = groups[group][sample]
    return final_groups


def read_exp(path, tdict):
    per = {}
    cols = []
    with open(path, 'r') as infile:
        line = infile.readline()
        cells = line.rstrip('\n').split(',')
        for i in range(len(cells)):
            if cells[i] == 'transcriptIDs':
                t_id = i
        for cell in cells:
            cols.append(cell.lstrip('FPKM.'))
        line = infile.readline()
        while line:
            cells = line.rstrip('\n').split(',')
            t = cells[t_id]
            if t in tdict:
                if tdict[t][0] not in per:
                    per[tdict[t][0]] = {}
                for i in range(len(cells[t_id:])-1):
                    if not cols[i+t_id+1] in per[tdict[t][0]]:
                        per[tdict[t][0]][cols[i+t_id+1]] = {'g': 0.0, 't': {}}
                    per[tdict[t][0]][cols[i+t_id+1]]['g'] += float(cells[i+t_id+1])
                    per[tdict[t][0]][cols[i+t_id+1]]['t'][t] = float(cells[i+t_id+1])
            line = infile.readline()
    infile.close()
    for gene in per:
        for sample in per[gene]:
            if per[gene][sample]['g'] > 0.0:
                for transcript in per[gene][sample]['t']:
                    per[gene][sample]['t'][transcript] = per[gene][sample]['t'][transcript]/per[gene][sample]['g']
    return per, cols[3:]


def count_genes(per, tdict):
    counts = {}
    for gene in per:
        for sample in per[gene]:
            if sample not in counts:
                counts[sample] = [0, 0]
            if per[gene][sample]['g'] > 0.0:
                counts[sample][1] += 1
                for transcript in per[gene][sample]['t']:
                    if per[gene][sample]['t'][transcript] > 0.5 and tdict[transcript][1] == 'Ensembl_canonical':
                        counts[sample][0] += 1
    for i in counts:
        print(i + '\t' + str(counts[i][0]) + '/' + str(counts[i][1]) + '\t' + str(counts[i][0]/counts[i][1]))
    return counts


def prepareData(exp, final_groups):
    x = [[], []]
    alttrace = []
    traces = {'canonical > 50%': [], 'canonical <= 50%': []}
    for group in final_groups:
        for i in ['Primary', 'Organoide', 'Xeno']:
            if i in final_groups[group]:
                x[0].append(group)
                x[1].append(i)
                traces['canonical > 50%'].append(exp[final_groups[group][i]][0])
                traces['canonical <= 50%'].append(exp[final_groups[group][i]][1])
                alttrace.append(exp[final_groups[group][i]][0]/exp[final_groups[group][i]][1]*100.0)
    return x, traces, alttrace


def plotExp(x, traces, alttrace):
    fig = go.Figure()
    i = 0
    for trace in traces:
        fig.add_bar(x=x, y=traces[trace], name=trace,)
        fig.update_layout(barmode='stack', yaxis_title='Number of Genes')
        i += 1
    fig.update_xaxes(tickangle=90)
    fig.show()
    fig.write_html('canonical_absolute.html')
    fig.write_image('canonical_absolute.svg', width=2000, height=1000)

    fig = go.Figure()
    i = 0

    fig.add_bar(x=x, y=alttrace,)
    fig.update_layout(barmode='stack', yaxis_title='[%] of Genes')
    i += 1
    fig.update_xaxes(tickangle=90)
    fig.show()
    fig.write_html('canonical_percent.html')
    fig.write_image('canonical_percent.svg', width=2000, height=1000)


if __name__ == '__main__':
    main()
