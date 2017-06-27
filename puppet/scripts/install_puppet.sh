#!/usr/bin/env bash

set -e

REPO_DEB="puppetlabs-release-pc1-xenial.deb"
if ! dpkg -s puppet-agent &>/dev/null; then
    echo "Installing puppet"
    wget https://apt.puppetlabs.com/${REPO_DEB}
    sudo dpkg -i ${REPO_DEB}
    rm ${REPO_DEB}
    sudo apt update
    sudo apt install puppet-agent
    /opt/puppetlabs/puppet/bin/gem install hiera-eyaml
fi