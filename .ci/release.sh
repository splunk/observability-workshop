#!/usr/bin/env bash

RESULT=$(curl -s -w "\n%{http_code}\n" \
  "https://api.github.com/repos/$TRAVIS_REPO_SLUG/releases" \
  -H "Authorization: token $api_key"  \
  -d @- <<EOF
{
  "tag_name": "$TRAVIS_TAG",
  "tag_commitish": "master"
}
EOF
)

if [ "$(tail -1 <<< "$RESULT")" != "201" ]; then
  echo FAILED
  echo "$RESULT"
  exit 1
fi

RELEASE_ID=$(sed -ne 's/^  "id": \(.*\),$/\1/p' <<< "$RESULT")
if [[ -z "$RELEASE_ID" ]]; then
  echo FAILED
  echo "$RESULT"
  exit 1
fi

echo SUCCESS
