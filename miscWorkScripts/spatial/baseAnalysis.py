import spatialdata as sd
from spatialdata_io import xenium
import matplotlib.pyplot as plt
import seaborn as sns
import scanpy as sc
import squidpy as sq
import argparse


def main():
    parser = argparse.ArgumentParser(description="plots Expression values")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input zarr Folder")
    parser.add_argument("-o", "--out", type=str, default=None, required=True,
                          help="Path to out directory.")
    args = parser.parse_args()

    sdata = sd.read_zarr(args.input)
    adata = sdata.tables["table"]
    adata = calcQCmetrics(adata, args.out)




def calcQCmetrics(adata, outpath):
    sc.pp.calculate_qc_metrics(adata, percent_top=(10, 20, 50, 150), inplace=True)
    cprobes = adata.obs["control_probe_counts"].sum() / adata.obs["total_counts"].sum() * 100
    cwords = adata.obs["control_codeword_counts"].sum() / adata.obs["total_counts"].sum() * 100
    with open(outpath + '/QC_statistics.txt', 'w') as out:
        out.write(f"Negative DNA probe count % : {cprobes}\n")
        out.write(f"Negative decoding count % : {cwords}\n")
    out.close()

    fig, axs = plt.subplots(1, 4, figsize=(15, 4))

    axs[0].set_title("Total transcripts per cell")
    sns.histplot(
        adata.obs["total_counts"],
        kde=False,
        ax=axs[0],
    )

    axs[1].set_title("Unique transcripts per cell")
    sns.histplot(
        adata.obs["n_genes_by_counts"],
        kde=False,
        ax=axs[1],
    )

    axs[2].set_title("Area of segmented cells")
    sns.histplot(
        adata.obs["cell_area"],
        kde=False,
        ax=axs[2],
    )

    axs[3].set_title("Nucleus ratio")
    sns.histplot(
        adata.obs["nucleus_area"] / adata.obs["cell_area"],
        kde=False,
        ax=axs[3],
    )

    fig.write(outpath + 'QC_statistics.svg')
    return adata


def processing(adata):
    adata.layers["counts"] = adata.X.copy()
    sc.pp.normalize_total(adata, inplace=True)
    sc.pp.log1p(adata)
    sc.pp.pca(adata)
    sc.pp.neighbors(adata)
    sc.tl.umap(adata)
    sc.tl.leiden(adata)

    sc.pl.umap(
        adata,
        color=[
            "total_counts",
            "n_genes_by_counts",
            "leiden",
        ],
        wspace=0.4,
    )


if __name__ == '__main__':
    main()
