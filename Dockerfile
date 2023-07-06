FROM mambaorg/micromamba:1.4.6
COPY . /app
WORKDIR /app
COPY --chown=$MAMBA_USER:$MAMBA_USER conda_env.yml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes
EXPOSE 8000
CMD ["gunicorn",  "umap_vis:server",  "-b", "8000"]
