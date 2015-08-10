from rest_framework import serializers
import json


class JsonField(serializers.WritableField):
    """
    A json field, we can use it for Postgres's new BSON fields.
    """

    def to_native(self, value):
        if isinstance(value, basestring):
            return json.loads(value)

        return value

    def from_native(self, value):
        if isinstance(value, basestring):
            return json.loads(value)

        return value

    @classmethod
    def to_json(cls, data):
        if isinstance(data, basestring):
            return json.loads(data)
        return data