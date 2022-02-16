#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
source ${SCRIPT_DIR}/utility.sh

DETACH=0
PYTHON_CODE=0
CI_MODE=0

# arg parse code references to
# https://stackoverflow.com/a/14203146
# https://www.inrhythm.com/building-command-line-tools-in-bash/
# https://medium.com/@Drew_Stokes/bash-argument-parsing-54f3b81a6a8f
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--detach)
      DETACH=1
      shift
      ;;
    -i|--ci)
      CI_MODE=1
      shift
      ;;
    *|-*|--*)
      echo "Unknown arguments $1"
      exit 1
      ;;
  esac
done


if [[ $DETACH -eq 0 ]]; then
  echo "Reading GitLab credential ..."
  source ${SCRIPT_DIR}/gitlab_credential.sh

  echo ${GITLAB_PASSWORD} | docker login -u ${GITLAB_USERNAME} --password-stdin $CI_REGISTRY
  docker build -t "${DOCKER_IMAGE_NAME}" . && docker image prune -f || { echo "Build failed"; exit 1; }
fi
