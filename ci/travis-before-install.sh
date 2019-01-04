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

if [ $TRAVIS_PULL_REQUEST = "false" ]
then
    branch=$TRAVIS_BRANCH
else
    branch=$TRAVIS_PULL_REQUEST_BRANCH
fi

echo branch ${branch}


for upstream_repo in vivarium vivarium_public_health
do

    upstream_branch="$(git ls-remote --heads https://github.com/ihmeuw/${upstream_repo}.git ${branch})"

    echo upstream branch found ${upstream_branch}

    if [ "${upstream_branch}" ]
    then
        git clone --branch=$branch https://github.com/ihmeuw/${upstream_repo}.git
        pushd ${upstream_repo}
        pip install .
        popd
    fi

done

popd


