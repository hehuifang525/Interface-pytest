#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

OUTPUT=--quiet
if [ "${1:-}" = '--show-diff' ]; then
    OUTPUT=
fi

# If a tagged version, just print that tag
HEAD_TAGS=$(git tag --points-at HEAD)
if [ -n "${HEAD_TAGS}" ] ; then
	echo ${HEAD_TAGS}
	exit 0
fi


WORKING_SUFFIX=$(if ! git diff --exit-code ${OUTPUT} HEAD >&2; \
                 then echo "-wip"; \
                 else echo ""; \
                 fi)
BRANCH_PREFIX=$(git rev-parse --abbrev-ref HEAD)

# replace spaces with dash
BRANCH_PREFIX=${BRANCH_PREFIX// /-}
# next, replace slashes with dash
BRANCH_PREFIX=${BRANCH_PREFIX//[\/\\]/-}
# now, clean out anything that's not alphanumeric or an dash
BRANCH_PREFIX=${BRANCH_PREFIX//[^a-zA-Z0-9-]/}
# finally, lowercase with TR
BRANCH_PREFIX=`echo -n $BRANCH_PREFIX | tr A-Z a-z`

echo "$BRANCH_PREFIX-$(git rev-parse --short HEAD)$WORKING_SUFFIX"

