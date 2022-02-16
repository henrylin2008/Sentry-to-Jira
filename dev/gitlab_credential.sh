SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")

CREDENTIAL_FILE=$(realpath "${SCRIPT_DIR}/../.gitlab-credential")

if [[ ! -f ${CREDENTIAL_FILE} ]]; then
  echo "GitLab credential file doesn't exist!"
  echo "Please follow the guidance to create the access token and save it locally."

  echo -n "Please enter your username of https://gitlab.i.wish.com: "
  read arg_username
  echo ""

  echo "Please go to https://gitlab.i.wish.com/profile/personal_access_tokens"
  echo "Choose a name of this access token, check 'read_registry' for Scopes, and click 'Create personal access token'"
  echo -n "Copy the generated access token, and paste it here: "
  read arg_password
  echo ""

  echo "Writing credential into ${CREDENTIAL_FILE}"
  printf "${arg_username}\n${arg_password}\n" > ${CREDENTIAL_FILE}
fi


gitlab_credential_lines=()
while IFS= read -r line || [[ "$line" ]]; do
  gitlab_credential_lines+=("$line")
done < ${CREDENTIAL_FILE}

export GITLAB_USERNAME=${gitlab_credential_lines[0]}
export GITLAB_PASSWORD=${gitlab_credential_lines[1]}
