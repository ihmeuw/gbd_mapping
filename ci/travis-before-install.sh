#!/bin/bash

uname -a
free -m
df -h
ulimit -a
mkdir builds
pushd builds

# Build into our own virtualenv
pip install -U virtualenv

virtualenv --python=python venv

source venv/bin/activate
python -V

pip install --upgrade pip setuptools

# For push builds, TRAVIS_BRANCH is the branch name
# For builds triggered by PR, TRAVIS_BRANCH is the branch targeted by the PR
branch=$TRAVIS_BRANCH
echo branch ${branch}

# iterate over upstream dependencies
for upstream_repo in vivarium vivarium_public_health
do
    upstream_branch_exists="$(git ls-remote --heads https://github.com/ihmeuw/${upstream_repo}.git ${branch})"

    # if there is a match for upstream, use that
    if [ ! -z "${upstream_branch_exists}" ]  # checks if not-empty
    then
        echo upstream branch found for ${branch} in ${upstream_repo}
        # clone and install upstream stuff if target branch exists
        git clone --branch=$branch https://github.com/ihmeuw/${upstream_repo}.git
        pushd ${upstream_repo}
        pip install .
        popd
    else
        echo no upstream branch found in ${upstream_repo}
    fi

done

popd

pip install .[test,docs]
