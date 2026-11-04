FROM python:3.12-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless curl ca-certificates git \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /workspaces/tgb_simulacao_modelagem_de_sistemas
COPY requirements.txt /tmp/tgb-requirements.txt
RUN pip install --no-cache-dir -r /tmp/tgb-requirements.txt
