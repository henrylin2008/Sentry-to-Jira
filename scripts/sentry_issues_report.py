import argparse
import logging
from sentry_alert_notifier.metrics.metrics_emitter import MetricsEmitter
from sentry_alert_notifier.sentry.client import SentryClient
from sentry_alert_notifier.project_config import ProjectConfig


def sentry_projects():
    return [
        ProjectConfig(
            name="merchant-backend-production",
            issue_count_threshold=1000,
        ),
        ProjectConfig(
            name="merchant-external-api",
            issue_count_threshold=50,
        ),
        ProjectConfig(
            name="merchant-frontend-production",
            issue_count_threshold=20,
        ),
    ]


def main(sentry_api_key):
    base_url = "https://sentry.infra.wish.com"
    sentry_client = SentryClient(base_url, sentry_api_key)
    emitter = MetricsEmitter()
    for project in sentry_projects():
        logging.info("fetching issues for project %s", project)
        issues = sentry_client.get_issues(project)
        count = len(issues)
        logging.info("%d issues found", count)
        emitter.emit_issues_count_for_project(project.name, count)
    emitter.push_metric_to_gateway("sentry_issues_count_monitor")


if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel("INFO")
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentry-api-key", dest='sentry_api_key', help="Sentry API Key", required=True)
    args = parser.parse_args()
    main(args.sentry_api_key)
