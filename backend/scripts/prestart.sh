#!/usr/bin/env bash
set -e
set -x

python app/backend_pre_start.py
alembic upgrade head
python app/initial_data.py

echo "✅ All prestart scripts completed"