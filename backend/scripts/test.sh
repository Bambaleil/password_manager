#!/usr/bin/env bash
set -e
set -x
echo "Begin test.sh"
coverage run --source=app -m pytest
coverage report --show-missing
coverage html --title "${@-coverage}"
