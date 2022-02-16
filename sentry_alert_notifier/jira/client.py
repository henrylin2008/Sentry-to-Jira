import requests
import json
import logging
from sentry_alert_notifier.requests_helper import RequestsHelper


class JiraClient(object):
    """
    Attributes:
        base_url (str): Jira API's base url
        auth_token (str): Auth token used to access Jira API
    """
    def __init__(self, base_url, auth_token):
        """
        Args:
            base_url (str): Jira API's base url
            auth_token (str): Auth token used to access Jira API
        """
        self.base_url = base_url
        self.auth_token = auth_token

    def send_request(self, endpoint, method, params=None):
        """
        Args:
            endpoint (str): the url where the request will be sent to
            method (str): the method for this request
            params (dict, optional): parameter used for querying, default to None
        Returns:
            dict: Response from the endpoint
        """
        method = method.upper()
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic {}".format(self.auth_token)
        }
        s = requests.Session()
        s.headers.update(headers)
        if params is None:
            params = {}

        response = None
        if method == "GET":
            response = RequestsHelper.requests_retry_session(session=s).get(
                endpoint, params=params
            )
        elif method == "POST":
            response = RequestsHelper.requests_retry_session(session=s).post(
                endpoint, data=params
            )

        if "application/json" in response.headers.get('content-type') and response.text:
            return json.loads(response.text)
        return None

    def get_issue(self, issue_id):
        """
        Args:
            issue_id (string): jira issue id
        Returns:
            dict: Info about the given issue
        """
        endpoint = "{base_url}/rest/api/2/issue/{issue_id}".format(base_url=self.base_url, issue_id=issue_id)
        result = self.send_request(endpoint, method="GET")
        return result

    def search_issue(self, query):
        """
        Args:
            query (string): JQL queries that define the search
        Returns:
            list: list of issues which satisfy the search condition
        """
        params = None
        if query:
            params = {
                'jql': query,
            }
        endpoint = "{base_url}/rest/api/2/search".format(base_url=self.base_url)
        result = self.send_request(endpoint, method="GET", params=params)
        return result.get("issues")

    def create_issue(self, params):
        """
        Args:
            params (string): info used to create jira issue
        Returns:
            dict: created jira issues
        """
        endpoint = "{base_url}/rest/api/2/issue".format(base_url=self.base_url)
        result = self.send_request(endpoint, method="POST", params=params)
        logging.debug("response from creating Jira ticket:\n %s", result)
        return result

    def add_watcher(self, issue_key, params):
        """
        Args:
            issue_key (str): the issue key corresponding to the jira ticket to be updated
            params (str): info of the watcher to be added
        """
        endpoint = "{base_url}/rest/api/2/issue/{issue_key}/watchers".format(
            base_url=self.base_url, issue_key=issue_key
        )
        self.send_request(endpoint, method="POST", params=params)

    def update_status(self, issue_key, status):
        """
        Args:
            issue_key (str): the issue key corresponding to the jira ticket to be updated
            status (str): the status id
        """
        params = {
          "transition": {
            "id": status
          }
        }
        endpoint = "{base_url}/rest/api/2/issue/{issue_key}/transitions".format(
            base_url=self.base_url, issue_key=issue_key
        )
        self.send_request(endpoint, method="POST", params=json.dumps(params))
