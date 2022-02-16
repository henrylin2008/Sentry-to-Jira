import attr


@attr.s
class ProjectConfig(object):
    name = attr.ib(type=str)
    sentry_params = attr.ib(type=dict, default=None)
    # only Sentry issues with count > issue_count_threshold would get a ticket
    issue_count_threshold = attr.ib(type=int, default=5000)
