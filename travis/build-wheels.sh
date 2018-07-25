#!/bin/bash
set -e -x

PY_VER_MAJOR=3
PY_VER_MINOR=7
PY_VER_PATCH=0

# hack to get current version of cmake
"/opt/python/cp${PY_VER_MAJOR}${PY_VER_MINOR}-cp${PY_VER_MAJOR}${PY_VER_MINOR}m/bin/pip" install cmake
export PATH="/opt/_internal/cpython-${PY_VER_MAJOR}.${PY_VER_MINOR}.${PY_VER_PATCH}/bin:${PATH}"

PYTHON_VERSIONS=(37 36 35)

# Compile wheels
for VERSION in "${PYTHON_VERSIONS[@]}"; do
    PYBIN="/opt/python/cp${VERSION}-cp${VERSION}m/bin"
    "${PYBIN}/pip" install -r /io/dev-requirements.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

for VERSION in "${PYTHON_VERSIONS[@]}"; do
    PYBIN="/opt/python/cp${VERSION}-cp${VERSION}m/bin"
    "${PYBIN}/pip" install mapbox_earcut --no-index -f /io/wheelhouse
done
