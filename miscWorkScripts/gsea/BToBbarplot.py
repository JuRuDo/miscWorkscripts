import numpy as np
import plotly.graph_objects as go
import math
import argparse


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="GSEA results in a table")
    parser.add_argument("-o", "--outfile", type=str, default=None, required=True,
                          help="Path to output file.")
    parser.add_argument("-d", "--delimiter", type=str, default='\t',
                          help="Table delimiter.")
    args = parser.parse_args()

    plotBar(args.input, args.outfile, args.delimiter)


def plotBar(path, outpath, d):
    data = {'Signature': [], 'Cluster': [], 'NES': [], 'padj': []}
    with open(path, 'r') as infile:
        lines = infile.readlines()
        n1 = lines[0].rstrip('\n').split(d)[1].split('#')[1]
        n2 = lines[0].rstrip('\n').split(d)[3].split('#')[1]
        genesets = []
        set1 = []
        set1_p = []
        set2 = []
        set2_p = []
        for line in lines[1:]:
            cells = line.rstrip('\n').split(d)
            genesets.append(cells[0])
            set1_p.append(min(-math.log10(float(cells[1])), 3))
            set1.append(float(cells[2]))
            set2_p.append(min(-math.log10(float(cells[3])), 3))
            set2.append(float(cells[4]))
    infile.close()
    y = list(range(len(set1)))

    fig = go.Figure(data=[
        go.Bar(y=y, x=set1, orientation='h', name=n1, base=0),
        go.Bar(y=y, x=set2, orientation='h', name=n2, base=0)
    ])

    fig.update_layout(
        barmode='stack',
        )

    fig.update_yaxes(
            ticktext=genesets,
            tickvals=y
        )
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
    fig.write_image(outpath + '.svg', width=800, height=400)
    fig.show()


if __name__ == '__main__':
    main()
