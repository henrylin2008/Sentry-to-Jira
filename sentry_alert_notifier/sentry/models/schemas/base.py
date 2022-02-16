from marshmallow import Schema, post_load
from abc import abstractproperty


class BaseSchema(Schema):

    @abstractproperty
    def data_class(self):
        pass

    @post_load
    def make_object_(self, data,):
        if not data or not isinstance(data, dict):
            return None
        return self.data_class(**data)
