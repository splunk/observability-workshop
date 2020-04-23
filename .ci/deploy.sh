#!/usr/bin/env bash

if [[ "${TRAVIS_PULL_REQUEST}" != "false" ]]; then
    echo "Not publishing docs for pull requests"
    exit 0
fi

HASH="$(git rev-parse HEAD)"
SHORT=$(git rev-parse --short HEAD)
MSG="Docs: $(git log -1 --pretty=format:'%s' "$HASH") ($SHORT via travis)"
DOCS_BRANCH=gh-pages

if git ls-remote origin $DOCS_BRANCH | grep -q $DOCS_BRANCH; then
    # docs branch already exists, clone it
    echo "Using existing docs branch"
    git clone --single-branch --branch $DOCS_BRANCH git@github.com:"$TRAVIS_REPO_SLUG".git ../site
    pushd ../site || exit
else
    echo "Creating docs branch"
    mkdir ../site
    pushd ../site || exit
    git init
    # create docs branch
    git checkout --orphan $DOCS_BRANCH
    touch .nojekyll
    git add .nojekyll
    git remote add origin git@github.com:"$TRAVIS_REPO_SLUG".git
fi

git config user.name "$GH_USER_NAME"
git config user.email "$GH_USER_EMAIL"
popd || exit

echo "Running mkdocs"

SITE_DIR=../site/$TRAVIS_TAG
mkdir -p "$SITE_DIR"
mkdocs build -v --site-dir "$SITE_DIR"
pushd ../site || exit

rm -f latest
ln -s "$TRAVIS_TAG" latest
git add "$TRAVIS_TAG" latest
git commit -m "$MSG"
echo "Pushing to GitHub pages"
git push origin $DOCS_BRANCH
popd || exit
