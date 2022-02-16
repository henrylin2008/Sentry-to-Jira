class SentryException(Exception):
    pass


class SentryHTTPException(SentryException):
    def __init__(self, http_error):
        super(SentryHTTPException, self).__init__()
        self.name = http_error.name
        self.msg = http_error.message


class SentryBadRequestException(SentryException):
    pass


class SentryEmptyResponseException(SentryException):
    pass
