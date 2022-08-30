from rest_framework import serializers


class NotSameValuesForFrields:
    requires_context = True

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message

    def check_parameters(self):
        if not isinstance(self.fields, (list, tuple)):
            raise TypeError(
                'Параметр fields валидатора NoTSameValuesForFields '
                'должен быть [list] или [tuple]'
            )
        for field in self.fields:
            if not isinstance(field, str):
                raise TypeError(
                    f'Неверный тип поля -{field}- должнен быть string'
                )
        if len(self.fields) != 2:
            raise KeyError(
                'В параметрe fields количество ключей не равно 2'
            )
        if not isinstance(self.message, str):
            raise TypeError(
                'Параметр [message] должен быть string'
            )

    def __call__(self, data, serializer):
        self.check_parameters()
        message = self.message or (
            f'Значение полей [{", ".join(self.fields)}] не может '
            f'быть одинаковым'
        )
        values = [
            value for key, value in data.items()
            if key in self.fields
        ]
        if values[0] == values[1]:
            raise serializers.ValidationError(message)
        return
