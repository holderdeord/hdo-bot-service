#!/usr/bin/env bash
set -e

ROOT="$(dirname $0)/.."

echo 'Parsing...'
puppet parser validate $(find modules/ manifests/ -name "*.pp")

echo 'Linting...'
puppet-lint --log-format "%{fullpath}:%{line} %{KIND} %{message}" \
  --no-documentation-check \
  --fail-on-warnings \
  {modules,manifests}/

# echo 'Linting yaml...'
# yaml-lint -q data/*.{eyaml,yaml}

echo "All good!"
