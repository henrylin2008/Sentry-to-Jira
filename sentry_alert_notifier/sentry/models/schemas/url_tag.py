from marshmallow import fields

from sentry_alert_notifier.sentry.models.schemas.base import BaseSchema
from sentry_alert_notifier.sentry.models.url_tag import URLTag


class URLTagSchema(BaseSchema):
    count = fields.Integer(allow_none=True)
    firstSeen = fields.DateTime(allow_none=True)
    lastSeen = fields.DateTime(allow_none=True)
    key = fields.String(allow_none=True)
    name = fields.String(allow_none=True)
    value = fields.String(allow_none=True)

    @property
    def data_class(self):
        return URLTag
