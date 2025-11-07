#!/bin/env python

import argparse
import math
import pandas as pd
import plotly.express as px




def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="GSEA results in a table")
    parser.add_argument("-o", "--outfile", type=str, default=None, required=True,
                          help="Path to output file.")
    parser.add_argument("-m", "--markersize", type=int, default=10, required=False,
                          help="Marker bubble size")
    args = parser.parse_args()


    data = readInput(args.input)
    plotBubble(data, args.outfile, args.markersize)


def readInput(path):
    data = {'Signature': [], 'NES': [], 'padj': [], 'Gene ratio': []}
    with open(path, 'r') as infile:
        lines = infile.readlines()
        tmp = []
        for x in lines[0].rstrip('\n').split('\t')[1:]:
            tmp.append(x.split('#'))
        for line in lines[1:]:
            cells = line.rstrip('\n').split('\t')
            genes = float(len(cells[7].split(' ')))
            data['Signature'].append(cells[0])
            data['Gene ratio'].append((genes/float(cells[6])))
            data['padj'].append(math.log10(float(cells[2])))
            data['NES'].append(float(cells[5]))
    infile.close()
    return pd.DataFrame(data)



def plotBubble(df, outpath, m):
    fig = px.scatter(df, x="NES", y="Signature",
                 size="Gene ratio", color="padj", size_max=m, color_continuous_scale='Bluered_r', range_color=(-3.0, 0.0))
    fig.update_layout(
        plot_bgcolor='white',
        font_color="black",
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        title='',
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        title='',
    )
    fig.update_traces(marker=dict(line=dict(width=1,
                                            color='black'), opacity=1.0,),
                      selector=dict(mode='markers'))
    fig.show()
    fig.write_image(outpath + '.svg', width=800, height=600)


if __name__ == '__main__':
    main()
