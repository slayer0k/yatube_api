from rest_framework import serializers


class NotSameValuesForFields:
    requires_context = True

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def check_fields(self, data):
        for field in self.fields:
            if field not in data:
                raise KeyError(
                    f'Поле -{field}- отсутствует в сериализаторе'
                )

    def __call__(self, data, serializer):
        self.check_fields(data.keys())
        message = self.message or (
            f'Значения полей [{", ".join(self.fields)}] не может '
            f'быть одинаковым'
        )
        values = {
            value for key, value in data.items()
            if key in self.fields
        }
        if len(values) != len(self.fields):
            raise serializers.ValidationError(message)
        return
