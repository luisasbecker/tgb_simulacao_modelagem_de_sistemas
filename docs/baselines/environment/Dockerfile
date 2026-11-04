FROM eclipse-temurin:21-jre
RUN apt-get update && apt-get install -y --no-install-recommends curl python3 ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY . .
RUN python3 scripts/validate_cfg.py
CMD ["./scripts/run_all.sh"]
