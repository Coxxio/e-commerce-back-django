import re
from rest_framework import serializers


class ValidatePassword:

    def __call__(self, value):
        # Aquí va tu lógica de validación
        errors = []
        if len(value) < 8:
            errors.append(
                "password must be longer than or equal to 8 characters")
        if re.match("^(?=.*?[A-Z])", value) == None:
            errors.append("password must have at least one capital letter")
        if re.match("^(?=.*?[a-z])", value) == None:
            errors.append("password must have at least one lowercase letter")
        if re.match("^(?=.*?[0-9])", value) == None:
            errors.append("password must have at least one number")
        if errors:
            raise serializers.ValidationError(errors)
        return value
