## Description

[Collector](https://github.com/Igor542/collector) is a simple telegram chat bot
to track money spending and help with payments.

## Usage

Example for `docker-compose`:

``` yaml
version: '3'
services:
    collector:
        image: collector:latest
        container_name: collector
        restart: always
        user: "1000:100"
        volumes:
          - "/path/to/secrets/TOKEN:/secrets/TOKEN:ro,Z"
          - "/path/to/storage:/storage:Z"
```

Replace user `id` and `gid` with the proper ones. Then run:

``` bash
docker-compose up -d
```

## How to build docker image locally

``` bash
docker build --no-cache -t collector . --build-arg BRANCH="master"
```
