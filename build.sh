#!/bin/bash

set -e

# Cleanup
rm -rf package || true
rm artifact.zip || true
poetry build
poetry run pip install --platform=manylinux2014_x86_64 --only-binary=:all: --upgrade -t package dist/*.whl
cd package ; zip -r ../artifact.zip . -x '*.pyc'
