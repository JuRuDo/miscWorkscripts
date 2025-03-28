#!/bin/env python

import argparse
import plotly.graph_objs as go


def main():
    parser = argparse.ArgumentParser(description="Merge multiple expression table with no headers")
    parser.add_argument("-i", "--infile", type=str, default=None, required=True,
                        help="list of input tables in tsv format")
    parser.add_argument("-o", "--outdir", type=str, default=None, required=True,
                        help="output table in tsv format")

    args = parser.parse_args()
    venndata = readinfile(args.infile)
    for entry in venndata:
        venn_to_plotly(venndata[entry], ["HaplotypeCaller", "FreeBayes", "DeepVariant"], args.outdir + '/Venn_' + entry)


def readinfile(path):
    venndata = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(' ')
            if cells[0] not in venndata:
                venndata[cells[0]] = [0, 0, 0, 0, 0, 0, 0]
            venndata[cells[0]][int(cells[1][4])-1] = int(cells[2])
    infile.close()
    return venndata


def venn_to_plotly(areas, labels, outname):
    fig = go.Figure()

    # Create scatter trace of text labels
    fig.add_trace(go.Scatter(
        x=[0.5, 1.5, 2.5, 1.5, 1.5, 0.85, 2.15, 0.7, 2.3, 1.5],
        y=[0.75, 1.3, 0.75, 0.6, 2.35, 1.7, 1.7, -0.2, -0.2, 3.1],
        text=[areas[0], areas[6], areas[1], areas[3], areas[2], areas[5], areas[4], labels[0], labels[1], labels[2]],
        mode="text",
        textfont=dict(
            color="black",
            size=18,
            family="Arail",
        )
    ))

    # Update axes properties
    fig.update_xaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )

    fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )

    # Add circles
    fig.add_shape(type="circle",
                  line_color="black",
                  x0=0, y0=0, x1=2, y1=2
                  )
    fig.add_shape(type="circle",
                  line_color="black",
                  x0=1, y0=0, x1=3, y1=2
                  )
    fig.add_shape(type="circle",
                  line_color="black",
                  x0=0.5, y0=0.9, x1=2.5, y1=2.9
                  )

    fig.update_shapes(opacity=0.3, xref="x", yref="y")

    fig.update_layout(
        height=690, width=600,
        plot_bgcolor="white"
    )
    fig.write_html(outname + '.html')
    fig.write_image(outname + '.svg', width=600, height=690)


if __name__ == '__main__':
    main()
