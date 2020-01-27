#!/bin/bash
set -e -x
cd /io

# Install prerequisites

IFS=',' read -ra PYTHONS <<< "$RELEASE_PYTHONS"
for PYTHON in "${PYTHONS[@]}"; do
    "${PYTHON}" -m pip install cython
done
"${PYTHONS[0]}" setup.py release
