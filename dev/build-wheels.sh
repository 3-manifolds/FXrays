#!/bin/bash
set -e -x
cd /io

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install -r dev/dev-requirements.txt
    "${PYBIN}/python" setup.py release --install
done

# Bundle external shared libraries into the wheels
#for whl in wheelhouse/*.whl; do
#    auditwheel repair "$whl" --plat $PLAT -w /io/wheelhouse/
#done

# Install packages and test
#for PYBIN in /opt/python/*/bin/; do
#    "${PYBIN}/pip" install FXrays --no-index -f /io/wheelhouse
#    "${PYBIN}/python" -m FXrays.test
#done
