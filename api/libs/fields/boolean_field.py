from rest_framework import serializers


class BooleanField(serializers.BooleanField):
    """
    A boolean field can have different formats depending on client.
    Better to manage it well.
    """
    TRUE_VALUES = ('true', 't', 'True', '1')
    FALSE_VALUES = ('false', 'f', 'False', '0')

    def from_native(self, value):
        if value in self.TRUE_VALUES:
            return True

        if value in self.FALSE_VALUES:
            return False

        return value