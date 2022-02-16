from marshmallow import fields
from marshmallow import pre_load

from sentry_alert_notifier.sentry.models.schemas.base import BaseSchema
from sentry_alert_notifier.sentry.models.schemas.issue_metadata import IssueMetaDataSchema
from sentry_alert_notifier.sentry.models.schemas.url_tag import URLTagSchema
from sentry_alert_notifier.sentry.models.issue import Issue


class IssueSchema(BaseSchema):
    id_ = fields.Integer()
    permalink = fields.String()
    culprit = fields.String(allow_none=True)
    metadata = fields.Nested(IssueMetaDataSchema, allow_none=True)
    title = fields.String(allow_none=True)
    urls = fields.List(fields.Nested(URLTagSchema), allow_none=True)
    count = fields.Integer(allow_none=True)
    firstSeen = fields.DateTime(allow_none=True)
    lastSeen = fields.DateTime(allow_none=True)

    @pre_load
    def process(self, data):
        # avoid using type as param in IssueMetadata class, which will shadow the built in 'type' function
        id_key = "id"
        id_val = data.get(id_key, None)
        data.pop(id_key, None)
        data["id_"] = id_val
        return data

    @property
    def data_class(self):
        return Issue
