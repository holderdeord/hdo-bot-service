#!/bin/bash
set -e

ROOT="$(dirname $0)/.."

# Bundle install unless we're already up to date.
bundle install --binstubs bin --path .bundle --quiet

${ROOT}/bin/librarian-puppet install --path=third-party
