
import scanpy as sc
import numpy as np
import h5py

# opening file in backed mode
adata = sc.read_h5ad("ea67253d-f1fb-4a3b-b6f1-3c6bd1f1a4b3.h5ad", backed='r')

# mask for cell selection
mask = (
        (adata.obs["cell_type_coarse"] == "Cancer cell") |
        (adata.obs["cell_type_coarse"] == "Epithelial cell")
)

idx = np.where(mask)[0]

infile = "ea67253d-f1fb-4a3b-b6f1-3c6bd1f1a4b3.h5ad"
outfile = "epithelial_cells_1.h5ad"

chunk_size = 100000
adata = None

with h5py.File(infile, "r") as f_in, h5py.File(outfile, "w") as f_out:

    X_in = f_in["X"]

    data_in = X_in["data"]
    indices_in = X_in["indices"]
    indptr_in = X_in["indptr"]

    shape = X_in.attrs["shape"]
    n_genes = shape[1]

    idx = np.asarray(idx)

    # ---- calculating row lengths
    row_lengths = indptr_in[idx +1] - indptr_in[idx]

    # ---- indptr output
    indptr_out = np.zeros(len(idx ) +1, dtype=indptr_in.dtype)
    indptr_out[1:] = np.cumsum(row_lengths)

    nnz = indptr_out[-1]

    print("New nnz:", nnz)

    # ---- Creating group X
    X_out = f_out.create_group("X")

    data_out = X_out.create_dataset(
        "data",
        shape=(nnz,),
        dtype=data_in.dtype,
        compression="gzip"
    )

    indices_out = X_out.create_dataset(
        "indices",
        shape=(nnz,),
        dtype=indices_in.dtype,
        compression="gzip"
    )

    X_out.create_dataset(
        "indptr",
        data=indptr_out
    )

    pos = 0

    # ---- copy chunked
    for start in range(0, len(idx), chunk_size):

        end = min(start + chunk_size, len(idx))
        idx_chunk = idx[start:end]

        starts = indptr_in[idx_chunk]
        ends = indptr_in[idx_chunk +1]

        lengths = ends - starts
        total = np.sum(lengths)

        chunk_idx = np.empty(total, dtype=np.int64)

        p = 0
        for s, e in zip(starts, ends):
            l = e - s
            chunk_idx[p: p +l] = np.arange(s, e)
            p += l

        data_out[pos:pos +total] = data_in[chunk_idx]
        indices_out[pos:pos +total] = indices_in[chunk_idx]

        pos += total

        print(f"Processed cells {start} - {end}")

    X_out.attrs["shape"] = (len(idx), n_genes)

    # ---- copy var
    f_in.copy("var", f_out)

    # ---- subset obs without pandas
    obs_in = f_in["obs"]
    obs_out = f_out.create_group("obs")

    for key in obs_in.keys():

        obs_out.create_dataset(
            key,
            data=obs_in[key][idx],
            compression="gzip"
        )

print("Done")

Test code

Andrea Guala
​Julian Dosch​



Dataset:



Icona h5ad ea67253 d -f1f b -
4a3 b -b6f 1 -
3c6bd1f1a4b3.h5ad