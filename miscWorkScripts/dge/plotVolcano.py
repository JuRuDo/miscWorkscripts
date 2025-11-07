#!/bin/env python

import argparse
import pandas as pd
import dash_bio
import numpy
import plotly.express as px


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="DGE file")
    parser.add_argument("-o", "--outpath", type=str, default=None, required=True,
                          help="output directory")
    parser.add_argument("-g", "--genelist", type=str, default=None, required=False,
                          help="genes of interest")
    parser.add_argument("-p", "--pvaluemin", type=float, default=0.000000000000000000005, required=False,
                          help="sets the min p value, all genes with lower value will be set to this value for plotting")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    df = df[df['padj'].notna()]
    df = df[df['gene'].notna()]

    df['capLFC'] = df.apply(set_max_log, axis=1)
    df['capP'] = df.apply(set_min_p, args=[args.pvaluemin], axis=1)

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


def set_max_log(row):
   if row['log2FoldChange'] > 10.0:
      return 10.0
   elif row['log2FoldChange'] < -10.0:
       return -10.0
   else:
       return row['log2FoldChange']


def set_min_p(row, minpvalue):
   if row['padj'] < minpvalue:
      return numpy.log10(minpvalue) * (-1)
   else:
       return numpy.log10(row['padj']) * (-1)


def labeled(row, genes):
    if row['gene'] in genes:
        return '1'
    else:
        return '0'


def vol_plot(df, out, genes):
    conditions = [
        (df['capLFC'] >= 1) & (df['padj'] <= 0.05),
        (df['capLFC'] <= -1) & (df['padj'] <= 0.05),
        False,
    ]
    df['Marker'] = numpy.select(conditions, ['0', '1', '2'], default='3')
    df = df.sort_values('Marker')

    fig = px.scatter(
        df[df['labeled']=='0'],
        x='capLFC',
        y='capP',
        color='Marker',
        color_discrete_sequence=['blue', 'red', 'grey'],
        hover_data=['gene', 'log2FoldChange', 'capP'],
        labels={
            "gene": "gene",
            "log2FoldChange": "log2(Fold Change)",
            "capP": "-log10(p-value)",
        },
    )
    if genes:
        fig3 = px.scatter(
            df[df['labeled']=='1'],
            x='capLFC',
            y='capP',
            color='Marker',
            color_discrete_sequence=['grey', 'blue', 'red'],
            text='gene',
            hover_data=['gene', 'log2FoldChange', 'capP'],
            labels={
                "gene": "gene",
                "log2FoldChange": "log2(Fold Change)",
                "capP": "-log10(p-value)",
            },
        )

        fig.add_trace(fig3.data[0])
    xmax = max(abs(min(df['log2FoldChange'])), max(df['log2FoldChange']))
    ymax = max(df['capP'])
    fig2 = px.line(
        x=[-8, 8, None, (-1) * 1, (-1) * 1, None, 1, 1],
        y=[1.3, 1.3, None, 0, ymax+2, None, 0, ymax+2],
    )
    fig2.update_traces(line=dict(color='black', width=1, dash='dash'))
    fig.update_traces(marker=dict(size=6, opacity=0.95))
    fig.add_trace(fig2.data[0])
    fig.update_layout(
        font=dict(size=16),
        plot_bgcolor='white',
        font_color="black",
        yaxis_range=[-0.1, ymax+0.1],
        xaxis_range=[-8-0.1, 8 + 0.1],
        title='',
        showlegend=False,

    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        title='logFC',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        title='-log10(Pvalue)',
        gridcolor='lightgrey'
    )
    fig.update_traces(
        textposition='top center',
    )
    fig.write_html(out + 'volcano_plot.html')
    fig.write_image(out + 'volcano_plot.svg', width=1200, height=800)
    fig.show()


def old_volcano(df, out):
    fig = dash_bio.VolcanoPlot(
        effect_size='capLFC',
        p='capP',
        snp='gene',
        gene='gene',
        dataframe=df,
        point_size=5,
        effect_size_line_color='black',
        genomewideline_color='black',
        genomewideline_value=1.3,
    )
    fig.update_layout(
        plot_bgcolor='white',
        font_color="black",
        yaxis_range=[-0.1, 20],
        xaxis_range=[-8.1, 8.1],
        title='',
        showlegend=False,

    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        title='logFC',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        linecolor='black',
        title='-log10(Pvalue)',
        gridcolor='lightgrey'
    )
    fig.show()
    fig.write_html(out + 'volcano_plot.html')
    fig.write_image(out + 'volcano_plot.svg', width=1200, height=1000)



if __name__ == '__main__':
    main()
