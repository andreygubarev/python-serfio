# syntax=docker/dockerfile:1
FROM debian:bookworm-slim

RUN apt-get update &&  \
    apt-get install -yq --no-install-recommends \
        ca-certificates \
        curl \
        serf \
        tini && \
    rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]

