# Structure visualization via UMAP embedding of MCES distances

This repository contains datasets from the Paper [Small molecule machine learning: All models are
wrong, some may not even be helpful](https://doi) alongside Jupyter Notebooks for visualization of
MCES distances. Files too large for GitHub are hosted at
[OSF](https://doi.org/10.17605/OSF.IO/5SXFE).

| file                               | description                                                                                                                                                                          |
|------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `biostructures.csv`                | Biomolecular structures (SMILES and InChI-key first block)                                                                                                                           |
| `biostructures_20k.csv`            | Subsample of biomolecular structures used throughout the paper                                                                                                                       |
| `subsampled_instances_20k.csv`     | Subsample of *pairs* of biomolecular structures used for runtime and threshold evaluations                                                                                           |
| `mces_distances.npz`               | Compressed numpy-object containing all computed MCES distances alongside SMILES. Hosted externally at [doi:10.17605/OSF.IO/5SXFE](https://doi.org/10.17605/OSF.IO/5SXFE).            |
| `umap_df.csv`                      | Computed UMAP embeddings for various datasets                                                                                                                                        |
| `umap_embedding_biostructures.pkl` | `umap-learn` object allowing projection of new structures onto the computed UMAP embedding. Hosted externally at [doi:10.17605/OSF.IO/5SXFE](https://doi.org/10.17605/OSF.IO/5SXFE). |

## Visualization

Visualization of precomputed UMAP embeddings as well as for new structures is possible via the
python-script [umap_vis.py](umap_vis.py). If you just want to use the visualization, download this
repository and run `python umap_vis.py`.

To project MCES distances of a new dataset onto the existing UMAP embedding, use the Jupyter
Notebook [umap_embedding.ipynb](umap_embedding.ipynb).

Python packages required are:
```
umap-learn
numba=0.53.1
pandas
numpy
plotly
rdkit
dash
gunicorn
```

A conda (or [mamba](https://github.com/mamba-org/mamba)) environment with all necessary packages
installed can be created with

```bash
conda env create -f conda_env.yml
# to activate:
conda activate umap_mces
```

## Docker

A docker container for the visualization can be built with the provided [Dockerfile](Dockerfile).

For the special case of self-hosting the docker container via reverse proxy, the environment
variable `PROXY_PREFIX_REQUESTS` might have to be set with the docker run option `docker run -e
PROXY_PREFIX_REQUESTS='...' ...`.
