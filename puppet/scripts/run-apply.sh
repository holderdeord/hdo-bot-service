#!/bin/bash

set -e

scripts/bootstrap.sh
scripts/install_puppet.sh
/opt/puppetlabs/bin/puppet apply --disable_warnings=deprecations --test --modulepath modules:third-party --hiera_config hiera.yaml manifests
