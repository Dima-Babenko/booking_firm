import re
from datetime import date
from django.core.exceptions import ValidationError

def validate_start_date(start_date: date) -> None:
    if start_date.year < 2025:
        raise ValidationError("Invalid created date - year must be created than 2025")