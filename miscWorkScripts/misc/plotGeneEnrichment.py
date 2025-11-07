#!/bin/env python

import argparse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="Protein Enrichment file")
    parser.add_argument("-o", "--outpath", type=str, default=None, required=True,
                          help="output directory")
    parser.add_argument("-g", "--genelist", type=str, default=None, required=False,
                          help="genes of interest")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    if args.genelist:
        genes = get_gois(args.genelist)
    else:
        genes = []
    df['labeled'] = df.apply(labeled, args=[genes], axis=1)

    vol_plot(df, args.outpath, genes)


def get_gois(path):
    genes = []
    with open(path, 'r') as infile:
        for line in infile.readlines():
            genes.append(line.rstrip('\n'))
    return genes


def labeled(row, genes):
    if row['Gene Name'] in genes:
        return '1'
    else:
        return '0'


def vol_plot(df, out, genes):
    fig3 = px.scatter(
        df[df['labeled']=='0'],
        x='Unique Peptides',
        y='log2 OE / Ctrl',
        color='labeled',
        color_discrete_sequence=['blue'],
        hover_data=['Gene Name', 'log2 OE / Ctrl', 'Unique Peptides'],
    )
    if genes:
        fig = px.scatter(
            df[df['labeled']=='1'],
            x='Unique Peptides',
            y='log2 OE / Ctrl',
            color='labeled',
            color_discrete_sequence=['red'],
            text='Gene Name',
            hover_data=['Gene Name', 'log2 OE / Ctrl', 'Unique Peptides'],
        )

        fig.add_trace(fig3.data[0])
    fig.update_traces(marker=dict(size=6, opacity=0.95))
    fig.update_layout(
        font=dict(size=16),
        plot_bgcolor='white',
        font_color="black",
        title='',
        showlegend=False,

    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        title='Unique Peptides',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        title='log2 OE / Ctrl',
        gridcolor='lightgrey'
    )
    fig.update_traces(
        textposition='top center',
    )
    fig.write_html(out + 'Gene_Scatter.html')
    fig.write_image(out + 'Gene_Scatter.svg', width=1200, height=800)
    fig.show()




if __name__ == '__main__':
    main()
