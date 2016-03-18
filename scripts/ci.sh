#!/bin/bash -xeu
PKG_NAME=${1:-${CI_REPO##*/}}
if [[ "$CI_BRANCH" =~ ^v[0-9]+.[0-9]?* ]]; then
    eval export ${PKG_NAME^^}_RELEASE_VERSION=\$CI_BRANCH
    echo ${CI_BRANCH} | tail -c +2 > __conda_version__.txt
fi
for PYTHON in python2.7 python3.4; do
    # $PYTHON setup.py sdist
    # $PYTHON -m pip install dist/*.tar.gz
    # (cd /; $PYTHON -m pytest --pyargs $PKG_NAME)
    ./scripts/run_tests.sh --cov $PKG_NAME --cov-report html
done
./scripts/coverage_badge.py htmlcov/ htmlcov/coverage.svg
! grep "DO-NOT-MERGE!" -R . --exclude ci.sh
