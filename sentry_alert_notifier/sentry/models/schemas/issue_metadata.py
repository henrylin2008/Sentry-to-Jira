from marshmallow import fields
from marshmallow import pre_load

from sentry_alert_notifier.sentry.models.issue_metadata import IssueMetaData
from sentry_alert_notifier.sentry.models.schemas.base import BaseSchema


class IssueMetaDataSchema(BaseSchema):
    type_ = fields.String(allow_none=True)
    value = fields.String(allow_none=True)

    @pre_load
    def process(self, data):
        # avoid using type as param in IssueMetadata class, which will shadow the built in 'type' function
        type_key = "type"
        type_val = data.get(type_key, None)
        data.pop(type_key, None)
        data["type_"] = type_val
        return data

    @property
    def data_class(self):
        return IssueMetaData
