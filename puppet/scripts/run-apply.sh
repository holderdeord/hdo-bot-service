#!/bin/bash

set -e

scripts/bootstrap.sh
scripts/install_puppet.sh
/opt/puppetlabs/bin/puppet apply --test --modulepath modules:third-party manifests
