import logging
import time

import requests

from sentry_alert_notifier.sentry.models.schemas.issue import IssueSchema
from sentry_alert_notifier.sentry.models.schemas.url_tag import URLTagSchema
from sentry_alert_notifier.project_config import ProjectConfig
from sentry_alert_notifier.requests_helper import RequestsHelper


class SentryClient(object):
    """
    Attributes:
        base_url (str): Sentry API's base url
        auth_token (str): Auth token used to access sentry API
    """

    def __init__(self, base_url, auth_token):
        """
        Args:
            base_url (str): Sentry API's base url
            auth_token (str): Auth token used to access sentry API
        """
        self.base_url = base_url
        self.auth_token = auth_token

    def send_request(self, endpoint, method, params=None, body=None):
        """
        Args:
            endpoint (str): the url where the request will be sent to
            method (str): http verb in upper case. i.e. GET, POST, PUT
            params (dict, optional): parameter used for querying, default to None
            body (dict, optional): request body
        Returns:
            Session: Response from the endpoint
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.auth_token)
        }
        s = requests.Session()
        s.headers.update(headers)

        if method == "GET":
            return RequestsHelper.requests_retry_session(session=s).get(
                endpoint, params=params
            )

        if method == "PUT":
            return RequestsHelper.requests_retry_session(session=s).put(
                endpoint,
                params=params,
                json=body,
            )

        if method == "POST":
            return RequestsHelper.requests_retry_session(session=s).post(
                endpoint,
                json=body,
            )

        raise Exception("Unsupported HTTP verb %s", method)

    def get_all_resources(self, endpoint, params=None):
        """
        Send GET request to an endpoint and handles pagination by traversing all 'next' pages
        Args:
            endpoint (str): the url where the request will be sent to
            params (dict, optional): parameter used for querying, default to None
        Returns:
            list: Response from the endpoint
        """
        results = []
        has_more_pages = True
        if params is None:
            params = {}
        while has_more_pages:
            response = self.send_request(endpoint, "GET", params)
            for entry in response.json():
                results.append(entry)
            has_more_pages = response.links.get("next") and response.links["next"]["results"] == "true"
            if has_more_pages:
                endpoint = response.links["next"]["url"]
        return results

    def get_events(self, project):
        """
        Args:
            project (string): project name in sentry API
        Returns:
            list: Response from Sentry Events API related to the project
        """
        endpoint = "{base_url}/api/0/projects/sentry/{project}/events/".format(base_url=self.base_url, project=project)
        results = self.get_all_resources(endpoint)
        return results

    def get_url_tags_for_an_issue(self, issue_id):
        """
        Args:
            issue_id (str): a sentry issue's id
        Returns:
            list: Response from Sentry Issues API which contains all url info related to the given issue
        """
        endpoint = "{base_url}/api/0/issues/{issue_id}/tags/url/values/".format(
            base_url=self.base_url,
            issue_id=issue_id,
        )
        responses = self.get_all_resources(endpoint)
        results = []
        for resp in responses:
            tag = URLTagSchema().load(resp).data
            if not tag:
                continue
            results.append(tag)
        return results

    def get_latest_event_for_an_issue(self, issue_id):
        """
        Args:
            issue_id (str): a sentry issue's id
        Returns:
            dict: Response from Sentry Issues API which contains the details of the latest event for an issue
        """
        endpoint = "{base_url}/api/0/issues/{issue_id}/events/latest/".format(base_url=self.base_url, issue_id=issue_id)
        resp = self.send_request(endpoint, "GET")
        result = resp.json()
        return result

    def get_issues(self, project):
        """
        Args:
            project (ProjectConfig): project name in sentry API
        Returns:
            list: Response from Sentry Issues API related to the project
        """
        endpoint = "{base_url}/api/0/projects/sentry/{project}/issues/".format(
            base_url=self.base_url, project=project.name
        )
        params = ["is:unresolved"]
        if project.sentry_params:
            params.extend(project.sentry_params)
        endpoint += "?query=" + " ".join(params)

        resp = self.get_all_resources(endpoint)
        results = [IssueSchema().load(result).data for result in resp]
        logging.info("%d issues fetched from Sentry", len(results))
        return results

    def resolve_issues(self, project, ids):
        """
        Resolve Sentry errors listed by ids
        Args:
            project (ProjectConfig): the sentry project object
            ids (list): a list of Sentry error IDs to resolve
        """
        chunk_size = 200
        itr = 0
        while itr < len(ids):
            start, end = itr, itr + chunk_size
            logging.info("processing ids[%d: %d]", start, end)
            chunk = ids[start: end]
            endpoint = "{base_url}/api/0/projects/sentry/{project}/issues/".format(
                base_url=self.base_url, project=project.name
            )
            id_params = {"id": [format(id_) for id_ in chunk]}
            payload = {"status": "resolved"}
            response = self.send_request(
                endpoint,
                "PUT",
                params=id_params,
                body=payload,
            )
            logging.info(response.json())
            itr += chunk_size
            time.sleep(2)
