#!/bin/bash

set -o errexit

pip3 install --upgrade setuptools pip wheel
pip3 install --user -r requirements-dev.txt
pre-commit install
pip install -e ."[azure, aws, google]"
