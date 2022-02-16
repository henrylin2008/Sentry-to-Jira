if [ ! -z ${ALREADY_SOURCED+x} ]; then
  return
fi
export ALREADY_SOURCED=1

export DOCKER_IMAGE_NAME="sentry_alert_notifier"

export CI_REGISTRY="registry-gitlab.i.wish.com"

export CI_PROJECT_ID="533"
export API_READ_TOKEN="npWHs13Hyy1Fz7RgXYA3"
export ENVIRONMENT="TESTING"

export LOCAL_PATH="$(pwd)"

export DOCKER_APP_PATH="/app"
export NODE_PATH="${DOCKER_APP_PATH}/node_modules"
export DOCKER_OUTPUT_PATH="${DOCKER_APP_PATH}/output"

export DOCKER_CMD_BASE="docker run --rm -t"
export DOCKER_MOUNT="-v \"${LOCAL_PATH}:${DOCKER_APP_PATH}\" -v \"${NODE_PATH}\""
export DOCKER_REGULAR_ENVS="-e PYTHONPATH=\"${PYTHONPATH}:/app\" -e CI_PROJECT_ID=\"${CI_PROJECT_ID}\" -e API_READ_TOKEN=\"${API_READ_TOKEN}\" -e ENVIRONMENT=\"${ENVIRONMENT}\""
export DOCKER_CI_ENVS="-e CI=\"true\" -e CI_COMMIT_SHA=\"$(git rev-parse HEAD)\" -e CI_COMMIT_REF_NAME=\"$(git rev-parse --abbrev-ref HEAD)\""

run_docker () {
  if [[ $CI_MODE -eq 1 ]]; then
    echo "Running in CI mode"
    run_ci_mode $@
  else
    echo "Running in local mode"
    run_local_mode $@
  fi
}

run_local_mode() {
  eval "${DOCKER_CMD_BASE}" "${DOCKER_MOUNT}" "${DOCKER_REGULAR_ENVS}" "${DOCKER_IMAGE_NAME}" "$@"
}

run_ci_mode() {
  eval "${DOCKER_CMD_BASE}" "${DOCKER_MOUNT}" "${DOCKER_REGULAR_ENVS}" "${DOCKER_CI_ENVS}" "${DOCKER_IMAGE_NAME}" "$@"
}
