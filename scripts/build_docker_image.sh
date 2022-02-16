#!/bin/sh

# script used OUTSIDE DOCKER CONTAINER to build docker image in gitlab ci

git diff --quiet origin/$CI_COMMIT_REF_NAME origin/master -- Dockerfile pip-requirements.txt; changes=$?

# This script is only called when gitlab thinks Dockerfile is changed. However,
# gitlab is weird and will still run the script for every new branch even if the
# Dockerfile is unchanged. So, only build new docker image if either:
#     1. There are changes in Dockerfile compared to origin/master
#     2. The branch is master itself (in which case the branch is not new,
#        so there must have been a change in Dockerfile)

if [ $changes -eq 1 ] || [ $CI_COMMIT_REF_NAME == 'master' ];
then
  echo "building"
  docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_NAME .
  docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_NAME
else
  echo "using old"
  docker pull $CI_REGISTRY_IMAGE:master
  docker tag $CI_REGISTRY_IMAGE:master $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_NAME
  docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_NAME
fi