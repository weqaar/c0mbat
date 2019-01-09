#!/usr/bin/env bash

echo "Cleaning up..."
find . -name '*.pyc' | xargs rm 2>/dev/null
find . -name '*.py~' | xargs rm 2>/dev/null
find . -name '*.out.txt' | xargs rm 2>/dev/null
find . -name '*.debug.log' | xargs rm 2>/dev/null
find . -name '*.error.log' | xargs rm 2>/dev/null
find . -name '*.stats.log' | xargs rm 2>/dev/null
rm -rf ./runtime/*
rm -rf ./cache/*
echo "Done."

