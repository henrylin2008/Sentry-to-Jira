from sentry_alert_notifier.metrics.sentry_metrics import SentryMetrics
from prometheus_client import CollectorRegistry, push_to_gateway


class MetricsEmitter(object):
    PUSH_GATEWAY = "http://pushgateway.infra.wish.com:9091"

    def __init__(self):
        self.registry = CollectorRegistry()

    def emit_issues_count_for_project(self, project, count, labels=None):
        """
        Args:
            project (string): Corresponding sentry project name
            count (int): sentry issue count
            labels (dict): the label name - label value mapping
        """
        metric_name = "{}_issues_count".format(project)
        SentryMetrics.gauge_set(metric_name, registry=self.registry, labels=labels, value=count)

    def push_metric_to_gateway(self, job):
        """
        Args:
            job (str): the corresponding job name for the metric
        """
        push_to_gateway(
            self.PUSH_GATEWAY,
            job=job,
            registry=self.registry,
        )
