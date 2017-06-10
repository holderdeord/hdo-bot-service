#!/bin/bash

set -e

puppet/scripts/bootstrap.sh
puppet/scripts/install_puppet.sh
puppet apply --test --modulepath modules:third-party manifests/site
