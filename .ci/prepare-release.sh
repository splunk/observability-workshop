#!/usr/bin/env bash

set -o errexit   # Exit on most errors
set -o errtrace  # Make sure any error trap is inherited
set -o nounset   # Disallow expansion of unset variables
set -o pipefail  # Use last non-zero exit code in a pipeline

dry_run=0
FLAVOUR=minor

while getopts 'nt:' opt; do
  case "$opt" in
    n)
      dry_run=1
      ;;
    t)
      FLAVOUR=${OPTARG}
      ;;
    *)
      echo 'Usage: prepare-release [ -n ] [ -t major|minor ]' >&2
      echo '  -n    do not perform any changes, dry-run'
      echo '  -t    type of release, one of major or minor (default)'
      exit 1
  esac
done

if [ $dry_run == 0 ]; then
  TAG=$(bumpversion --list "$FLAVOUR" | awk -F= '/new_version=/ { print $2 }')
else
  TAG=$(bumpversion --dry-run --list "$FLAVOUR" | awk -F= '/new_version=/ { print $2 }')
fi

# add new version to mkdocs yaml
awk "/versions:/ { print; print \"  - v$TAG\";next }1" mkdocs.yml |
# limit list of version in mkdocs.yaml to last two
awk '(s==0) { print } (s==1) { if (c&&c--) print; } /versions:/ {s=1;c=2} /^$/ { if (c <= 0 && s==1) { c=1;s=0;print; } }' > mkdocs.new.yml
if [ $dry_run == 0 ]; then
  mv mkdocs.new.yml mkdocs.yml
fi
# add new version to README
awk "/Previous versions of the workshop are also available:/ { print; print \"- [v$TAG](https://signalfx.github.io/observability-workshop/v$TAG/)\";next }1" README.md |
# limit list of version in README to last two
awk "NR==1,/Previous versions of the workshop are also available:/{c=3} c&&c-- " > README.md

if [ $dry_run == 0 ]; then
  git fetch --tags origin
  git add README.md  mkdocs.yml
  git commit --amend -m "Releasing v$TAG"
  git tag -a "v$TAG" -m "Version $TAG"
  # separate push and push tag to allow the push to fail. we will not push the tag, allowing to fix the release before it happens
  # git push --follow-tags origin master
  git push origin master || { echo 'Push failed. git pull --rebase from upstream and attempt another release.'; exit 1; }
  git push --tags
fi
