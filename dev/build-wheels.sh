#!/bin/bash
set -e -x

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install -r /fxrays/dev/dev-requirements.txt
    "${PYBIN}/pip" wheel /fxrays/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat $PLAT -w /fxrays/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install FXrays --no-index -f /fxrays/wheelhouse
    "${PYBIN}/python" -m FXrays.test
done
