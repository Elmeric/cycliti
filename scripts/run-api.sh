#! /usr/bin/env bash

# Exit in case of error
set -e

cd ~/code/cycliti/backend/app
source ~/.cache/pypoetry/virtualenvs/app-LSx8f5tU-py3.12/bin/activate
fastapi run
