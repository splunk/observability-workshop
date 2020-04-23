#!/usr/bin/env bash

HASH="$(git rev-parse HEAD)"
MSG="$(git log -1 --pretty=format:'Docs: %s ({sha} via travis)' "$HASH")"
DOCS_BRANCH=gh-pages2
export HASH MSG

git remote set-url origin git@github.com:"$TRAVIS_REPO_SLUG".git

# git remote set-branches --add origin $DOCS_BRANCH
# git fetch origin && git fetch origin $DOCS_BRANCH:$DOCS_BRANCH

git clone --single-branch --branch $DOCS_BRANCH "$(git config remote.origin.url)" ../site
pushd ../site || exit
git config user.name "$GH_USER_NAME"
git config user.email "$GH_USER_EMAIL"
git checkout $DOCS_BRANCH || git checkout --orphan $DOCS_BRANCH
popd || exit

if [ "${TRAVIS_PULL_REQUEST}" = "false" ]; then
  echo "Running mkdocs"
  # mkdocs gh-deploy -v --clean -m "$MSG" --remote-name origin

  SITE_DIR=../site/$TRAVIS_TAG
  mkdir -p "$SITE_DIR"
  touch "$SITE_DIR/.nojekyll"
  mkdocs build --site-dir "$SITE_DIR"
  cd ../site || exit

  git add "$TRAVIS_TAG"
  git commit -m "$MSG"
  echo "Pushing to GitHub pages"
  git push origin $DOCS_BRANCH
fi
