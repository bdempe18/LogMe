import re

from django.core.exceptions import ValidationError
from django.db import models


class HexColorField(models.CharField):
    """
    Custom model field for storing hex color codes.
    """

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 7  # Hex codes are 7 characters (#RRGGBB)
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not re.match(r"^#[0-9a-fA-F]{6}$", value):
            msg = f"{value} is not a valid hex color code."
            raise ValidationError(msg)

    def from_db_value(self, value, expression, connection):
        # Ensure the value is always returned in uppercase from the database
        return value.upper() if value else value

    def to_python(self, value):
        # Ensure the value is always stored in uppercase
        return value.upper() if value else value
