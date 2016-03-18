#!/bin/bash
touch doc/_build/html/.nojekyll
p LICENSE doc/_build/html/.nojekyll
git config --global user.name "drone"
git config --global user.email "drone@nohost.com"
mkdir -p deploy/public_html/branches/"${CI_BRANCH}" deploy/script_queue
cp -r htmlcov/ doc/_build/html/ deploy/public_html/branches/"${CI_BRANCH}"/
