#!/bin/env python


import plotly.express as px
import argparse


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input folder containing htseq files.")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    args = parser.parse_args()

    data, x, y = read_input(args.input)
    print(y)
    data = normalizeRows(data)
    print(x)
    plotHeatmap(data, x, y, args.output)


def normalizeRows(data):
    newdata = []
    for i in data:
        tmp = []
        for x in i:
            tmp.append(x / max(i))
        newdata.append(tmp)
    return newdata


def read_input(path):
    data = []
    y = []
    with open(path, 'r') as infile:
        line = infile.readline()
        cells = line.rstrip('\n').split(',')
        x = cells[1:]
        line = infile.readline()
        while line:
            cells = line.rstrip('\n').split(',')
            y.append(cells[0])
            tmp = []
            for n in cells[1:]:
                tmp.append(float(n))
            data.append(tmp)
            line = infile.readline()
    return data, x, y


def plotHeatmap(data, x, y, name):
    fig = px.imshow(data, x=x, y=y, color_continuous_scale='RdBu_r', aspect="auto")
    fig.update_xaxes(side="top")
    fig.show()
    fig.write_html(name + '.html')
    fig.write_image(name + '.svg', width=800, height=600)
    fig.write_image(name + '.png', width=800, height=600)


if __name__ == '__main__':
    main()
