#!/usr/bin/env bash

HASH="$(git rev-parse HEAD)"
MSG="$(git log -1 --pretty=format:'Docs: %s ({sha} via travis)' "$HASH")"
export HASH MSG