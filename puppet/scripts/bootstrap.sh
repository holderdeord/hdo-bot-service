#!/bin/bash
set -e

# Bundle install unless we're already up to date.
bundle install

librarian-puppet install --path=third-party
