from rest_framework import serializers


class NotSameValuesForFields:
    requires_context = True

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def __call__(self, data, serializer):
        message = self.message or (
            f'Значения полей [{", ".join(self.fields)}] не может '
            f'быть одинаковым'
        )
        values = [
            value for key, value in data.items()
            if key in self.fields
        ]
        for index in range(len(values)):
            if values.pop(0) in values:
                raise serializers.ValidationError(message)
        return
