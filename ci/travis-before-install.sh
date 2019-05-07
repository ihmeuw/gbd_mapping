#!/bin/bash

uname -a
free -m
df -h
ulimit -a
mkdir builds
pushd builds

# Build into our own virtualenv
pip install -U virtualenv

virtualenv --python=python venv

source venv/bin/activate
python -V

pip install --upgrade pip setuptools

# gbd_mapping has no upstream github dependencies
popd
pip install .[test,docs]
