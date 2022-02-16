import attr


@attr.s
class IssueMetaData(object):
    type_ = attr.ib(type=str, default=None)
    value = attr.ib(type=str, default=None)
