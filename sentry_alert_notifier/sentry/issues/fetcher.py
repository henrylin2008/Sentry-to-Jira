import logging
import urlparse

from sentry_alert_notifier.sentry.client import SentryClient
from sentry_alert_notifier.code_owner_processor import CodeOwnerProcessor
from sentry_alert_notifier.sentry.issue_filter import non_connection_issues
from sentry_alert_notifier.sentry.models.schemas.stack_trace import StackTraceSchema
from sentry_alert_notifier.project_config import ProjectConfig
from sentry_alert_notifier.sentry.issue_filter import filter_frequent_issues
from concurrent.futures import ThreadPoolExecutor


def _build_latest_event_map(issues, sentry_client):
    future_jobs = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for issue in issues:
            future_jobs.append(
                (
                    issue,
                    executor.submit(
                        sentry_client.get_latest_event_for_an_issue, issue.id_
                    ),
                )
            )
    ret = {}
    for issue, future_job in future_jobs:
        ret[issue.id_] = future_job.result()
    return ret


def get_sentry_issues(sentry_client, project, code_owner_str):
    """
    Args:
        sentry_client (SentryClient): Sentry project client
        project (ProjectConfig): sentry project name
        code_owner_str (str): the CODEOWNERS string
    Returns:
        list: list of issues used for cutting tickets
    """
    issues = sentry_client.get_issues(project)
    issues = non_connection_issues(issues)
    logging.info("%s issues left after skipping connection related errors", len(issues))
    issues = filter_frequent_issues(issues, project.issue_count_threshold)
    logging.info("%s issues left after skipping infrequent errors", len(issues))

    latest_event_map = _build_latest_event_map(issues, sentry_client)

    # get and set more metadata on Sentry issues
    for issue in issues:
        issue_id = issue.id_
        metadata = issue.metadata
        if not metadata:
            continue

        # retrieve & set latest event so that we have stacktrace info
        # make this extra API call here to avoid unnecessary queries on issues
        # that do not need a Jira ticket
        event_dict = latest_event_map.get(issue.id_)
        if not event_dict:
            logging.warn("failed to get latest event for issue %s", issue.id_)
            continue

        entries = event_dict.get("entries")
        stack_trace_list = []
        for entry in entries:
            if entry.get("type") == "exception":
                stack_trace_list = entry.get("data").get("values")[0].get("stacktrace").get("frames")
        stack_traces = StackTraceSchema(many=True).load(stack_trace_list).data
        issue.stack_traces = stack_traces

        # set most related url
        urls = sentry_client.get_url_tags_for_an_issue(issue_id)
        if urls:
            issue.urls = urls
            urls = sorted(issue.urls, key=lambda i: i.count, reverse=True)
            issue.most_counted_url = urlparse.urlparse(urls[0].value).path

    code_owner_processor = CodeOwnerProcessor(code_owner_str)
    code_owner_processor.assign_owners(issues)
    return issues
