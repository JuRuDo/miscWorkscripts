#!/bin/env python


import scanpy as sc
import celltypist
from celltypist import models
import argparse


def main():
    parser = argparse.ArgumentParser(description="Processes sce data from a h5ad file, needs a Patient and Type obs "
                                                 "column")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input data as h5ad file.")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    args = parser.parse_args()

    sc.set_figure_params(figsize=(5, 5))
    adata = sc.read_h5ad(args.input)
    adata.obs['Sample'] = adata.obs['Patient'].astype(str) + '_' + adata.obs['Type'].astype(str)
    adata = genetypes(adata)
    adata = filter(adata)
    adata = normalize(adata)
    sc.set_figure_params(figsize=(5, 5), format='svg')
    adata = pca(adata)
    adata = cluster(adata)
    adata = ct_run(adata)
    sc.write(args.output, adata)



def genetypes(adata):
    # mitochondrial genes, "MT-" for human, "Mt-" for mouse
    adata.var["mt"] = adata.var_names.str.startswith("MT-")
    # ribosomal genes
    adata.var["ribo"] = adata.var_names.str.startswith(("RPS", "RPL"))
    # hemoglobin genes
    adata.var["hb"] = adata.var_names.str.contains("^HB[^(P)]")

    sc.pp.calculate_qc_metrics(
        adata, qc_vars=["mt", "ribo", "hb"], inplace=True, log1p=True
    )

    sc.pl.violin(
        adata,
        ["n_genes_by_counts", "total_counts", "pct_counts_mt"],
        jitter=0.4,
        multi_panel=True,
        save='_counts.pdf',
        show=False
    )

    sc.pl.scatter(adata, "total_counts", "n_genes_by_counts", color="pct_counts_mt", save='_counts.pdf',
                  show=False)
    return adata


def filter(adata):
    sc.pp.filter_cells(adata, min_genes=100)
    sc.pp.filter_genes(adata, min_cells=3)
    sc.pp.scrublet(adata, batch_key="Sample")
    return adata


def normalize(adata):
    # Saving count data
    adata.layers["counts"] = adata.X.copy()
    # Normalizing to median total counts
    sc.pp.normalize_total(adata)
    # Logarithmize the data
    sc.pp.log1p(adata)
    sc.pp.highly_variable_genes(adata, n_top_genes=2000, batch_key="Sample")
    sc.pl.highly_variable_genes(adata, save='.pdf', show=False)
    return adata


def pca(adata):
    sc.tl.pca(adata)
    sc.pl.pca(
        adata,
        color=["Sample", "Sample", "pct_counts_mt", "pct_counts_mt"],
        dimensions=[(0, 1), (2, 3), (0, 1), (2, 3)],
        ncols=2,
        size=2,
        save='_QC.svg',
        show=False
    )
    # Nearest neighbor graph constuction and visualization
    sc.pp.neighbors(adata)
    sc.tl.umap(adata)
    sc.pl.umap(
        adata,
        color="Sample",
        # Setting a smaller point size to get prevent overlap
        size=2,
        save='_Sample.svg',
        show=False
    )
    return adata


def cluster(adata):
    sc.tl.leiden(adata, flavor="igraph", n_iterations=2)
    sc.pl.umap(adata, color=["leiden"], save='_Leiden.svg', show=False)
    sc.pl.umap(
        adata,
        color=["leiden", "predicted_doublet", "doublet_score"],
        # increase horizontal space between panels
        wspace=0.5,
        size=3,
        save='_Leiden_doublet.svg',
        show=False
    )
    return adata


def ct_run(adata):
    adata_celltypist = ct_prepare(adata)
    model_low, model_high = ct_models()

    predictions_high = ct_predict(adata_celltypist, model_high)
    adata.obs["celltypist_cell_label_coarse"] = predictions_high.obs.loc[
        adata.obs.index, "majority_voting"
    ]
    adata.obs["celltypist_conf_score_coarse"] = predictions_high.obs.loc[
        adata.obs.index, "conf_score"
    ]

    predictions_low = ct_predict(adata_celltypist, model_low)
    adata.obs["celltypist_cell_label_fine"] = predictions_low.obs.loc[
        adata.obs.index, "majority_voting"
    ]
    adata.obs["celltypist_conf_score_fine"] = predictions_low.obs.loc[
        adata.obs.index, "conf_score"
    ]

    ct_plot(adata)
    return adata


def ct_prepare(adata):
    adata_celltypist = adata.copy()  # make a copy of our adata
    adata_celltypist.X = adata.layers["counts"]  # set adata.X to raw counts
    sc.pp.normalize_total(
        adata_celltypist, target_sum=10**4
    )  # normalize to 10,000 counts per cell
    sc.pp.log1p(adata_celltypist)  # log-transform
    return adata_celltypist


def ct_models():
    models.download_models(
        force_update=True, model=["Immune_All_Low.pkl", "Immune_All_High.pkl"]
    )

    model_low = models.Model.load(model="Immune_All_Low.pkl")
    model_high = models.Model.load(model="Immune_All_High.pkl")
    return model_low, model_high


def ct_predict(adata_celltypist, model):
    predictions = celltypist.annotate(
        adata_celltypist, model=model, majority_voting=True
    )

    predictions_adata = predictions.to_adata()
    return predictions_adata


def ct_plot(adata):
    sc.pl.umap(
        adata,
        color=["celltypist_cell_label_coarse", "celltypist_conf_score_coarse"],
        frameon=False,
        sort_order=False,
        wspace=1,
        save='_CT_coarse.svg',
        show=False
        )

    sc.pl.umap(
        adata,
        color=["celltypist_cell_label_fine", "celltypist_conf_score_fine"],
        frameon=False,
        sort_order=False,
        wspace=1,
        save='_CT_fine.svg',
        show=False
    )


    if __name__ == '__main__':
        main()
