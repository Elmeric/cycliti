#! /usr/bin/env bash

# Let the DB start
# python /app/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
cd app
export PYTHONPATH=/home/eric/code/cycliti/backend/app
python initial_data.py
cd ..
