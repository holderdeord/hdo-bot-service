#!/usr/bin/env bash

set -e

REPO_DEB="puppet5-release-xenial.deb"
if ! dpkg -s puppet-agent &>/dev/null; then
    echo "Installing puppet"
    wget https://apt.puppetlabs.com/${REPO_DEB}
    sudo dpkg -i ${REPO_DEB}
    rm ${REPO_DEB}
    sudo apt update
    sudo apt install puppet-agent
fi

if ! /opt/puppetlabs/puppet/bin/gem list --installed hiera-eyaml &>/dev/null; then
    echo "Installing hiera-eyaml"
    /opt/puppetlabs/puppet/bin/gem install hiera-eyaml
fi