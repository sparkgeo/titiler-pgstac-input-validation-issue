#!/bin/bash -e


tester_image_name="local/titiler-pgstac-tester:postgres-16"
docker build \
    --tag $tester_image_name \
    --build-arg PGSTAC_IMAGE=local/pgstac:postgres-16 \
    --file Dockerfile.tester \
    .

docker run \
    --rm \
    --tty \
    $tester_image_name \
    uv run pytest -x -s -vv
