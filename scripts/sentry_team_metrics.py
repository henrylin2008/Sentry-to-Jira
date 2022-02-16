import argparse
import logging
from collections import defaultdict
from sentry_alert_notifier.sentry.client import SentryClient
from sentry_alert_notifier.project_config import ProjectConfig
from sentry_alert_notifier.sentry.issues.fetcher import get_sentry_issues
from sentry_alert_notifier.team_preference import team_preference
from os import path
from prometheus_client import CollectorRegistry, push_to_gateway
from sentry_alert_notifier.metrics.sentry_metrics import SentryMetrics


def sentry_projects():
    return [
        ProjectConfig(
            name="merchant-backend-production",
            issue_count_threshold=0,
        ),
        ProjectConfig(
            name="merchant-external-api",
            issue_count_threshold=0,
        ),
        ProjectConfig(
            name="merchant-frontend-production",
            issue_count_threshold=0,
        ),
    ]


def count_issues(issues):
    no_owner = "no_owner"
    ret = defaultdict(list)
    team_pref = team_preference()
    for issue in issues:
        github_team = issue.owner
        team = team_pref.get(github_team)
        if not team:
            team_name = no_owner
        else:
            team_name = team.name
        ret[team_name].append(issue)
    return ret


def code_owner_str():
    ret = None
    file_path = path.join(__file__, "../../sentry_alert_notifier/__tests__/resources/CODEOWNER.txt")
    with open(path.abspath(file_path), "r") as f:
        ret = f.read()
    return ret


def main(sentry_api_key):
    base_url = "https://sentry.infra.wish.com"
    sentry_client = SentryClient(base_url, sentry_api_key)
    registry = CollectorRegistry()
    gauge = SentryMetrics.create_gauge(
        'error_team_stats',
        'Summarize Sentry errors per team',
        ["team", "project"],
        registry,
    )
    event_gauge = SentryMetrics.create_gauge(
        'error_total_events_team_stats',
        'Summarize Total Events of Sentry errors per team',
        ["team", "project"],
        registry,
    )
    for project in sentry_projects():
        logging.info("fetching issues for project %s", project)
        issues = get_sentry_issues(sentry_client, project, code_owner_str())
        team_count = count_issues(issues)
        for team_name, issue_list in team_count.iteritems():
            gauge.labels(
                team=team_name,
                project=project.name,
            ).set(len(issue_list))

            # emit event metrics
            event_count = sum([issue.count for issue in issue_list])
            event_gauge.labels(
                team=team_name,
                project=project.name,
            ).set(event_count)

            logging.info("Sentry issues owned by %s:", team_name)
            for issue in issue_list:
                logging.info(issue.permalink)

    # push all gauges to gateway server
    push_to_gateway(
        "http://pushgateway.infra.wish.com:9091",
        job='sentry_error_team_counter',
        registry=registry,
    )


if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel("INFO")
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentry-api-key", dest='sentry_api_key', help="Sentry API Key", required=True)
    args = parser.parse_args()
    main(args.sentry_api_key)
