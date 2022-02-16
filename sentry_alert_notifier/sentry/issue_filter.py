from datetime import datetime
from datetime import timedelta
import pytz
from sentry_alert_notifier.team_preference import team_preference


SKIPPED_STATUS = "Resolved, Closed, Done, Invalid, Wontfix, Duplicate, Declined, Cancelled, Completed"


def connection_issue_types():
    return {
        "UDPTimeout",
        "TimeoutError",
        "StreamClosedError",
        "RPCException",
        "DNSError",
    }


def connection_predicate(issue):
    return issue.metadata.type_ in connection_issue_types()


def non_connection_predicate(issue):
    return not connection_predicate(issue)


def legacy_predicate(issue):
    now = pytz.utc.localize(datetime.utcnow())
    return issue.lastSeen < now - timedelta(days=10)


def _filter(issues, predicate):
    return [issue for issue in issues if predicate(issue)]


def non_connection_issues(issues):
    return _filter(issues, non_connection_predicate)


def connection_issues(issues):
    return _filter(issues, connection_predicate)


def legacy_issues(issues):
    """
    Args:
        issues (list): a list of Sentry Issue obj
    Returns:
        a list of issues what have occurred within the past 10 days
    """
    return _filter(issues, legacy_predicate)


def filter_frequent_issues(issues, threshold):
    """
    Returns a list of issues who occurrence count is greater than the threshold
    Args:
        issues (list): a list of Issue object
        threshold (int): the threshold

    Returns:
        list: a list of issues

    """
    return [
        issue for issue in issues if issue.count > threshold
    ]


def filer_ownerless_issues(issues):
    team_pref = team_preference()
    ret = []
    for issue in issues:
        if issue.owner not in team_pref:
            ret.append(issue)
    return ret


def filter_new_issues(jira_client, sentry_issues):
    ret = []
    for sentry_issue in sentry_issues:
        sentry_issue_link = sentry_issue.permalink
        query = "summary ~ \"{sentry_issue_link}\" AND status NOT IN ({skipped_status})".format(
            sentry_issue_link=sentry_issue_link,
            skipped_status=SKIPPED_STATUS,
        )
        # skip issues already created with an active status
        jira_task = jira_client.search_issue(query)
        if jira_task:
            continue

        ret.append(sentry_issue)
    return ret
