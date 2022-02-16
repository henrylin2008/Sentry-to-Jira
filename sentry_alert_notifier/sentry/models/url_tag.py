import attr
from datetime import datetime


@attr.s
class URLTag(object):
    key = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    value = attr.ib(type=str, default=None)
    count = attr.ib(type=int, default=None)
    firstSeen = attr.ib(type=datetime, default=None)
    lastSeen = attr.ib(type=datetime, default=None)
