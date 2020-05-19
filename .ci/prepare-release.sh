#!/usr/bin/env bash

set -o errexit   # Exit on most errors
set -o errtrace  # Make sure any error trap is inherited
set -o nounset   # Disallow expansion of unset variables
set -o pipefail  # Use last non-zero exit code in a pipeline

FLAVOUR=${1:-minor}
TAG=$(bumpversion --list "$FLAVOUR" | awk -F= '/new_version=/ { print $2 }')

awk "/versions:/ { print; print \"  - v$TAG\";next }1" mkdocs.yml > mkdocs.new.yml
mv mkdocs.new.yml mkdocs.yml
awk "/Previous versions of the workshop are also available:/ { print; print \"- [v$TAG](https://signalfx.github.io/app-dev-workshop/v$TAG/)\";next }1" README.md |
awk "NR==1,/Previous versions of the workshop are also available:/{c=3} c&&c-- " > README.new.md

mv README.new.md README.md

git fetch --tags origin
git add README.md  mkdocs.yml
git commit --amend -m "Releasing v$TAG"
git tag -a "v$TAG" -m "Version $TAG"
git push --follow-tags origin master
