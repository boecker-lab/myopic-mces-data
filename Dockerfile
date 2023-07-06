FROM mambaorg/micromamba:1.4.6
COPY --chown=$MAMBA_USER:$MAMBA_USER conda_env.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes
EXPOSE 8050
CMD ["python", "umap_vis.py"]
