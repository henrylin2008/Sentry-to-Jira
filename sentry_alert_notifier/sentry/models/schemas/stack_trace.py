from marshmallow import fields

from sentry_alert_notifier.sentry.models.schemas.base import BaseSchema
from sentry_alert_notifier.sentry.models.stack_trace import StackTrace


class StackTraceSchema(BaseSchema):
    file_name = fields.String(load_from="filename")
    line_num = fields.Integer(load_from="lineNo")

    @property
    def data_class(self):
        return StackTrace
