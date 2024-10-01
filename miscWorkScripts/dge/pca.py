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



import pandas as pd
import argparse
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from pkg_resources import get_distribution
import json


def do_pca(pca_DF, ntop, threshold):
    """
    This function applies PCA on the given DataFrame containing expression
    data. The overall information content vector and principal components
    for all replicates under all conditions will be returned.

    DataFrame: the DataFrame containing expression value.
    replicates: the list of replicates for each condition.

    """

    selector = VarianceThreshold()
    b = selector.fit(pca_DF)
    c = sorted(list(b.variances_))
    c.reverse()
    print(len(c))
    print(c[ntop])
    print(c[ntop+1])
    selector = VarianceThreshold(threshold=threshold)
    selector = selector.set_output(transform="pandas")
    new_df = selector.fit_transform(pca_DF)

    features = list(new_df.columns)
    print(len(features))
    x = new_df.loc[:, features].values
    x = StandardScaler().fit_transform(x)
    n_repl = len(new_df)
    pca = PCA(n_components=n_repl)
    column = []
    for i in range(n_repl):
        column.append("PC" + str(i + 1))
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=principalComponents
                               , columns=column, index=new_df.index.values.tolist())
    # Generate the dictionary for general information content of PCs.
    info_content = pca.explained_variance_ratio_
    info_contentDf = pd.DataFrame(data=info_content
                                  , columns=["information_content"]
                                  , index=column).T
    result_info = info_contentDf.to_dict("index")["information_content"]
    # Add replicate PC coordinates
    repl = principalDf.iloc[0:len(new_df)].to_dict("index")
    return {"PC_info": result_info, "data": repl}


def read_data(epath):
    df = pd.read_csv(epath, delimiter='\t', header=0, index_col=0)
    return df.T


def main():
    version = get_distribution('workScripts').version
    parser = argparse.ArgumentParser(description='You are running SpICE version ' + str(version) + '.',
                                     epilog="This script does the PCA from the results of the SpICE pipeline.")
    required = parser.add_argument_group('required arguments')
    parser.add_argument('--version', action='version', version=str(version))
    required.add_argument("-i", "--countPath", default=None, type=str, required=True,
                          help="path to the normalized counts")
    required.add_argument("-o", "--outpath", default=None, type=str, required=True,
                          help="path to output file")
    required.add_argument("-n", "--ntop", default=500, type=int,
                          help="select n top feature based on variance")
    required.add_argument("-t", "--threshold", default=0, type=int,
                          help="threshold")
    args = parser.parse_args()

    pca_df = read_data(args.countPath)
    result_info = do_pca(pca_df, args.ntop, args.threshold)
    jsonOut = json.dumps(result_info, indent='    ')
    f = open(args.outpath, 'w')
    f.write(jsonOut)
    f.close()


if __name__ == '__main__':
    main()
