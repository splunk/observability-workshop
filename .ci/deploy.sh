#!/usr/bin/env bash

HASH="$(git rev-parse HEAD)"
MSG="$(git log -1 --pretty=format:'Docs: %s ({sha} via travis)' "$HASH")"
export HASH MSG

git config user.name "$GH_USER_NAME"
git config user.email "$GH_USER_EMAIL"
git remote set-url origin git@github.com:signalfx/app-dev-workshop.git

git remote set-branches --add origin gh-pages
git fetch origin && git fetch origin gh-pages:gh-pages
if [ "${TRAVIS_PULL_REQUEST}" = "false" ]; then
  echo "Pushing to github";
  mkdocs gh-deploy -v --clean -m "$MSG" --remote-name origin
  git push origin gh-pages;
fi
