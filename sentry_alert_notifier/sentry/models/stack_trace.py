import attr


@attr.s
class StackTrace(object):
    file_name = attr.ib(type=str)
    line_num = attr.ib(type=int)
