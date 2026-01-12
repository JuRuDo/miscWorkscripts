#!/bin/env python


import argparse
import math
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Performs logRank test by using groups based on protein expression")
    parser.add_argument("-s", "--survivalData", type=str, default=None, required=True,
                          help="input table with survival data.")
    parser.add_argument("-e", "--expressionData", type=str, default=None, required=True,
                          help="input table with protein expression data.")
    parser.add_argument("-u", "--upperlimit", type=float, default=0.25, required=False,
                          help="sets the portion of samples that are considered part of the upper group, default is the"
                               " upper quartile (0.25)")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output directory.")
    args = parser.parse_args()
    sur = pd.read_csv(args.survivalData, sep="\t", index_col=0)
    exp = pd.read_csv(args.expressionData, sep="\t", index_col=0)
    upper = math.ceil(len(list(exp.columns)) * args.upperlimit)
    Path(args.output + '/figures').mkdir(parents=True, exist_ok=True)
    out = {'pval': [], 'statistic': []}
    for i in range(len(exp.index)):
        x, y = defineGroups(exp, upper, exp.index[i], sur)
        res = logRankTest(x, y, i, args.output)
        out['pval'].append(res.pvalue)
        out['statistic'].append(res.statistic)
    df = pd.DataFrame(out, index=exp.index)
    df.sort_values(by=['pval'], inplace=True)
    df.to_csv(args.output + '/results.csv')
    df = pd.DataFrame(exp.index)
    df.to_csv(args.output + '/index.csv')


def defineGroups(exp, upper, protein, sur):
    exp.sort_values(by=[protein], axis=1, inplace=True, ascending=False)
    uncensored = []
    right = []
    censor_c = sur.columns[0]
    sur_c = sur.columns[1]
    for i in list(exp.columns)[:upper]:
        if int(sur[sur_c][i]):
            uncensored.append(int(sur[censor_c][i]))
        else:
            right.append(int(sur[censor_c][i]))
    x = stats.CensoredData(uncensored=uncensored, right=right)
    uncensored = []
    right = []
    for i in list(exp.columns)[upper:]:
        if int(sur[sur_c][i]):
            uncensored.append(int(sur[censor_c][i]))
        else:
            right.append(int(sur[censor_c][i]))
    y = stats.CensoredData(uncensored=uncensored, right=right)
    return x, y


def logRankTest(x, y, i, output):
    res = stats.logrank(x=x, y=y)
#    if res.pvalue < 0.05:
    ax = plt.subplot()
    ecdf_x = stats.ecdf(x)
    ecdf_x.sf.plot(ax, label='upper')
    ecdf_y = stats.ecdf(y)
    ecdf_y.sf.plot(ax, label='lower')
    ax.set_xlabel('Time to death (weeks)')
    ax.set_ylabel('Empirical SF')
    plt.legend()
    plt.savefig(output + '/figures/' + str(i) + '.png')
    plt.close()
    return res


if __name__ == '__main__':
    main()
