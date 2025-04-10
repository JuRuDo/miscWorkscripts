#!/bin/env python

#######################################################################
# Copyright (C) 2022 Julian Dosch
#
# This file is part of .
#
#  SpICE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SpICE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with expNet.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################


import argparse
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def main():
    parser = argparse.ArgumentParser(description="create line plot that shows which regions of a sequence have ")
    parser.add_argument("-d", "--dge", type=str, default=None, required=True,
                          help="DGE file")
    parser.add_argument("-o", "--out", type=str, default=None, required=True,
                          help="output directory")
    parser.add_argument("-g", "--genes", type=str, default=None, required=True,
                          help="gene position table, needs geneID [0] and start [1], ordered by start")
    parser.add_argument("-w", "--windowsize", type=int, default=2000000,
                          help="Size of the sliding window")
    parser.add_argument("-s", "--stepsize", type=int, default=50000,
                          help="Defines how much the window slides with each step")
    parser.add_argument("-t", "--title", type=str, default="Chr",
                          help="Title and filename of the plot")
    parser.add_argument("--expressedGenes", action="store_false",
                          help="Use only expressed genes instead of all annotated genes for total number")
    parser.add_argument("--start", type=int, default=0,
                          help="Region start")
    parser.add_argument("--stop", type=int, default=1000000000,
                          help="Region stop")
    parser.add_argument("-r", "--reg", type=str, default="a",
                          help="take all [a], only upregulated [+], or only downregulated [-]")
    args = parser.parse_args()

    if args.reg == "+":
        mode = 1
    elif args.reg == "-":
        mode = 2
    elif args.reg == "a":
        mode = 0
    else:
        print("unknown --reg option, continuing with 'a'")
        mode = 0
    genes, first, last = readChr(args.genes)
    dge, down = readDGE(args.dge, mode)
    siggenes, numgenes, steps, numDgeGenes, down, numDgeDownGenes = calcPlotData(
        genes, first, last, dge, down, args.windowsize, args.stepsize, args.expressedGenes, args.start, args.stop)
    plotChrDE(siggenes, numgenes, numDgeGenes, down, numDgeDownGenes, steps, args.title, args.out)


def readChr(path):
    genes =  []
    first = None
    last = 0
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split('\t')
            if not first:
                first = int(cells[1])
            if int(cells[1]) > last:
                last = int(cells[1])
            genes.append((int(cells[1]), cells[0]))
    infile.close()
    return genes, first, last


def readDGE(path, mode):
    dge = {}
    down = {}
    with open(path, 'r') as infile:
        for line in infile.readlines():
            cells = line.rstrip('\n').split(',')
            if not cells[0].strip('"') == 'gene':
                if cells[3] == "NA":
                    dge[cells[0].strip('"')] = False
                    down[cells[0].strip('"')] = False
                else:
                    if mode == 1:
                        dge[cells[0].strip('"')] = float(cells[4]) <= 0.05 and float(cells[2]) > 0.5
                        down[cells[0].strip('"')] = False
                    elif mode == 2:
                        dge[cells[0].strip('"')] = float(cells[4]) <= 0.05 and float(cells[2]) < -0.5
                        down[cells[0].strip('"')] = False
                    else:
                        dge[cells[0].strip('"')] = float(cells[4]) <= 0.05
                        down[cells[0].strip('"')] = float(cells[4]) <= 0.05 and float(cells[2]) < -0.5

    infile.close()
    return dge, down


def calcPlotData(genes, first, last, dge, downdge, windowSize, stepSize, allgenes, start, stop):
    current = max(start, first)
    currentGene = 0
    siggenes = []
    numgenes = []
    downgenes = []
    numDgeGenes = []
    numDgeDownGenes = []
    steps = []
    while current < min(last, stop):
        if genes[currentGene][0] >= current:
            if currentGene < len(genes)-1:
                i = currentGene
                sig = 0.0
                down = 0.0
                numg = 0
                cont = True
                while genes[i][0] <= current + windowSize and cont:
                    if genes[i][1] in dge:
                        numg += 1
                        if dge[genes[i][1]]:
                            sig += 1.0
                        if downdge[genes[i][1]]:
                            down += 1.0
                    elif allgenes:
                        numg += 1
                    if i == len(genes)-2:
                        cont = False
                    i += 1
                if numg > 0:
                    sig = sig/numg
                    down = down/numg
                siggenes.append(sig*100)
                downgenes.append(down*100)
                numgenes.append(numg)
                numDgeGenes.append(numg*sig)
                numDgeDownGenes.append(numg*down)
                steps.append(int((current+stepSize/2)))
                current += stepSize
            else:
                current += stepSize
        else:
            currentGene += 1
    return siggenes, numgenes, steps, numDgeGenes, downgenes, numDgeDownGenes


def plotChrDE(siggenes, numgenes, numDgeGenes, down, numDgeDownGenes, steps, title, out):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=steps, y=numgenes, marker=dict(color="Grey", opacity=0.2), name="Genes total"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(x=steps, y=numDgeGenes, marker=dict(color="Green", opacity=0.9), name="DGE genes"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(x=steps, y=numDgeDownGenes, marker=dict(color="Orange", opacity=0.9), name="Downregulated genes"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=steps, y=siggenes, name="DE genes [%]",line=dict(color="Green")),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(x=steps, y=down, name="Downregulated [%]",line=dict(color="Orange")),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text=title,
        title_x=0.5,

        barmode='overlay',
        plot_bgcolor='white',
    )
    # Set x-axis title
    fig.update_xaxes(title_text="Position",ticks='outside', linecolor='black',)

    # Set y-axes titles
    fig.update_yaxes(title_text="DE genes [%]", ticks='outside', linecolor='black', secondary_y=True, range=[0,100])
    fig.update_yaxes(title_text="Genes per window", ticks='outside', linecolor='black',secondary_y=False)

    fig.write_html(out + '/' + title + '.html')
    fig.write_image(out + '/' + title + '.svg', width=1200, height=800)


if __name__ == '__main__':
    main()
