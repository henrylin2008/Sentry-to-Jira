import attr
from datetime import datetime


@attr.s
class IssueDetail(object):
    type_ = attr.ib(type=str, default=None)
    title = attr.ib(type=str, default=None)
    first_seen = attr.ib(type=datetime, default=None)
    last_seen = attr.ib(type=datetime, default=None)
    clickable_url = attr.ib(type=str, default=None)
    count = attr.ib(type=int, default=0)
    details = attr.ib(type=str, default=None)
