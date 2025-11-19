# Structure visualization via UMAP embedding of myopic MCES distances

This repository contains datasets from the publication [Coverage bias in small molecule machine learning](https://doi.org/10.1038/s41467-024-55462-w) ([citation](https://github.com/AlBi-HHU/myopic-mces#citation)) alongside Jupyter Notebooks for visualization of myopic
MCES distances. Files too large for GitHub are hosted at
[OSF](https://doi.org/10.17605/OSF.IO/5SXFE). See the [main repository](https://github.com/AlBi-HHU/myopic-mces) for computation of myopic MCES distances.

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
repository and run `python umap_vis.py`. A small web service for the visualization is running at [https://mces-data.boeckerlab.uni-jena.de/](https://mces-data.boeckerlab.uni-jena.de/).

To project MCES distances of a new dataset onto the existing UMAP embedding, use the Jupyter
Notebook [umap_embedding.ipynb](umap_embedding.ipynb).

A python installation with version >= 3.9 is required (3.9.18 is was used in development). Packages required are:
```
umap-learn=0.5.3
numba=0.53.1
scipy=1.7.1
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

![Visualization example](visualization_example.gif)

## Docker

A docker container for the visualization can be built with the provided [Dockerfile](Dockerfile).

For the special case of self-hosting the docker container via reverse proxy, the environment
variable `PROXY_PREFIX_REQUESTS` might have to be set with the docker run option `docker run -e
PROXY_PREFIX_REQUESTS='...' ...`.
