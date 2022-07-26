#!/usr/bin/env bash
set -o errexit

rm -rf docs/*
pdoc --html --config show_source_code=False --output-dir docs renameit
mv docs/renameit/* docs
rm -r docs/renameit
