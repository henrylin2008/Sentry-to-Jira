from prometheus_client import Gauge


class JiraMetrics(object):
    @classmethod
    def get_metric(cls):
        return "marketplace_jira"

    @classmethod
    def fix_metric_name(cls, metric_name):
        """
        Args:
            metric_name (string): metric name
        Returns:
            string: metric name where space and dash char are replaced
        """
        result = "_"
        metric_name = metric_name.replace(" ", "_")
        metric_name = metric_name.replace("-", "_")
        result += metric_name
        return result

    @classmethod
    def build_metric_name(cls, metric_name):
        """
        Args:
            metric_name (string): metric name
        Returns:
            string: the complete metric name
        """
        if metric_name == "":
            return cls.get_metric()
        metric = cls.fix_metric_name(metric_name)
        result = cls.get_metric()
        result += metric
        return result

    @classmethod
    def gauge_set(cls, metric_name, registry, value=1):
        """
        Args:
            metric_name (string): metric name
            registry (CollectorRegistry): registry for the metric
            value (float, optional): The value which Gauge will set. Defaults to 1
        """
        metric = cls.build_metric_name(metric_name)
        Gauge(metric, "jira tickets", registry=registry).set(value)
