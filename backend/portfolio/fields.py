import json

from django.db import models


class ResolutionField(models.TextField):

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return None
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None

    def get_prep_value(self, value):
        if value is None:
            return None
        return json.dumps(value)
