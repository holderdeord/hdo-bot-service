#!/bin/bash

set -e

scripts/bootstrap.sh
scripts/install_puppet.sh
puppet apply --test --modulepath modules:third-party manifests
