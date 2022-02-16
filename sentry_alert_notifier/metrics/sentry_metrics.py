from prometheus_client import Gauge


class SentryMetrics(object):
    @classmethod
    def get_metric(cls):
        return "marketplace_sentry"

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
    def create_gauge(cls, metric_name, description, labels, registry):
        metric = cls.build_metric_name(metric_name)
        gauge = Gauge(
            metric,
            description,
            labelnames=labels,
            registry=registry,
        )
        return gauge

    @classmethod
    def gauge_set(cls, metric_name, registry, labels=None, value=1):
        """
        note: This method does not allow setting different values for different labels.
              Use create_gauge() then set value manually. i.e.
              gauge = SentryMetrics.create_gauge(
                  'error_team_stats',
                  'Summarize Sentry errors per team',
                  ["label1", "label2", ...],
                  CollectorRegistry(),
              )
              // all 'label' below must be defined when creating the gauge
              for label, label_val, metric_val in my_tuple:
                gauge.labels(label=label_val).set(metric_val)
        Args:
            metric_name (string): metric name
            registry (CollectorRegistry): registry for the metric
            labels (dict): the label name - label value mapping
            value (int, optional): The value which Gauge will set. Defaults to 1
        """
        metric = cls.build_metric_name(metric_name)
        if labels:
            label_list = labels.keys()
            gauge = Gauge(
                metric,
                "sentry issues count",
                labelnames=label_list,
                registry=registry,
            )
            gauge.labels(**labels).set(value)
        else:
            gauge = Gauge(
                metric,
                "sentry issues count",
                registry=registry,
            )
            gauge.set(value)
