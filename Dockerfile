FROM mambaorg/micromamba:1.4.6
COPY --chown=$MAMBA_USER:$MAMBA_USER conda_env.yml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes
COPY . /app
WORKDIR /app
EXPOSE 8050
ENV PROXY_PREFIX=
CMD ["gunicorn",  "umap_vis:server",  "--bind", "0.0.0.0:8050"]
