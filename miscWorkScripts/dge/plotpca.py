import pandas as pd
import argparse
from pkg_resources import get_distribution
import json
import plotly.express as px


def prepare_pca_plot_data(pca_data, resultinfo, cond, pc1_id, pc2_id, pc3_id):
    pc1 = pc1_id + f' {resultinfo[pc1_id]:.4f}'
    pc2 = pc2_id + f' {resultinfo[pc2_id]:.4f}'
    pc3 = pc3_id + f' {resultinfo[pc3_id]:.4f}'
    plot_data = {pc1: [], pc2: [], pc3: [], 'Condition': [], 'Sample': []}
    print(cond)
    for replicate in pca_data:
        plot_data[pc1].append(pca_data[replicate][pc1_id])
        plot_data[pc2].append(pca_data[replicate][pc2_id])
        plot_data[pc3].append(pca_data[replicate][pc3_id])
        plot_data['Condition'].append(cond[replicate]["Condition"])
        plot_data['Sample'].append(replicate)
    return plot_data, pc1, pc2, pc3


def create_pca_plot(pc, pc1, pc2, pc3, out):
    df = pd.DataFrame(pc)
    n_colors = len(df['Condition'].unique())
    colors = px.colors.sample_colorscale('Rainbow', [n/(n_colors -1) for n in range(n_colors)])
    fig1 = px.scatter(df, x=pc1, y=pc2, color='Condition', hover_data=['Condition', 'Sample'],
                         color_discrete_sequence=colors)
    fig1.update_layout(font=dict(size=14), legend={'itemsizing': 'constant'})
    fig1.show()
    fig1.write_html(out + '/PCA_' + pc1.split(' ')[0] + pc2.split(' ')[0] + pc3.split(' ')[0] + '.html')


def read_data(pca_path, cond_path):
    cond = pd.read_csv(cond_path, delimiter=',', header=0)
    cond['Condition'] = cond['Line'] + '#' + cond['Model']
    cond = cond.set_index('id').T.to_dict()
    pca = read_json(pca_path)
    return pca, cond


def read_json(path):
    with open(path, 'r') as infile:
        in_dict = json.loads(infile.read())
    return in_dict


def main():
    version = get_distribution('workScripts').version
    parser = argparse.ArgumentParser(description='You are running SpICE version ' + str(version) + '.',
                                     epilog="This script does the PCA from the results of the SpICE pipeline.")
    required = parser.add_argument_group('required arguments')
    parser.add_argument('--version', action='version', version=str(version))
    required.add_argument("-i", "--pca_data", default=None, type=str, required=True,
                          help="path to the pca results")
    required.add_argument("-c", "--conditions", default=None, type=str, required=True,
                          help="A file containing a list of conditions to be considered for the PCA.")
    required.add_argument("-o", "--outpath", default=None, type=str, required=True,
                          help="path to output dir")
    required.add_argument("-p", "--pcs", default=['PC1', 'PC2', 'PC3'], type=str, nargs=3,
                          help="Which PCs to plot, requires 3 PCs: PC1 PC2 PC3")
    args = parser.parse_args()

    pca, cond = read_data(args.pca_data, args.conditions)
    plot_data, pc1, pc2, pc3 = prepare_pca_plot_data(pca["data"], pca["PC_info"], cond, args.pcs[0], args.pcs[1],
                                                     args.pcs[2])
    create_pca_plot(plot_data, pc1, pc2, pc3, args.outpath)

