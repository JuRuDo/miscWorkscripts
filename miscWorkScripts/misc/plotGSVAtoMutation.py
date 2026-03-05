#!/bin/env python

import argparse
import pandas as pd
import plotly.express as px


def main():
    parser = argparse.ArgumentParser(description="Get length of all transcripts")
    parser.add_argument("-i", "--gsva", type=str, default=None, required=True,
                        help="gsva csv file")
    parser.add_argument("-m", "--mutation", type=str, default=None, required=True,
                        help="mutation status gsva file")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                        help="output directory")
    args = parser.parse_args()

    gsva = readGSVA(args.gsva)
    mutations = readMutations(args.mutation)
    df = pd.merge(gsva, mutations, left_index=True, right_index=True, how="right")
    for i in gsva:
        fig = px.box(df, x='All', y=i, labels={'All':'Mutations', i:'GSVA score'}, points='all', title=i)
        fig.update_layout(
            font=dict(size=16),
            plot_bgcolor='white',
            font_color="black",
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            linecolor='black',
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            linecolor='black',
        )
        fig.update_traces(marker=dict(
                color='White',
                size=5,
                line=dict(
                    color='Black',
                    width=1
                )
            ),
            line_color='Black',
            line_width=1,
            fillcolor='White',
        )
        fig.write_image(args.output + '/' + str(i) + '.svg')
        fig.write_image(args.output + '/' + str(i) + '.png')


def readMutations(path):
    df = pd.read_csv(path, sep="\t", index_col=0)
    return df['All'].replace(1, 'mutated').replace(0, 'normal')


def readGSVA(path):
    df = pd.read_csv(path, sep=",", index_col=0)
    return df.transpose()