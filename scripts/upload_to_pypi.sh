#!/usr/bin/env bash

# script used INSIDE DOCKER CONTAINER to upload the generated
# Python client (and models) to the internal PyPi server
OUTPUT_PATH="$*"
curr_path="$(pwd)"
echo "model output path = ${OUTPUT_PATH}"
mkdir -p OUTPUT_PATH
cd "${OUTPUT_PATH}"

python setup.py sdist

ls -altr "${OUTPUT_PATH}"

echo "uploading via twine"
echo "PYPI_SERVER = ${PYPI_SERVER}"
twine upload --verbose --repository-url $PYPI_SERVER -u "$USERNAME" -p $PASSWORD dist/* #remember to switch when ready

cd ${curr_path}