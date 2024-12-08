import re
from django.core.exceptions import ValidationError


def validate_no_special_characters(value):

    if not re.match("^[a-zA-Z0-9\s.,!?-]*$", value):
        raise ValidationError(
            'Only letters, numbers, and basic punctuation are allowed.'
        )


def validate_due_date_after_start_date(start_date, due_date):
    if due_date and start_date and due_date < start_date:
        raise ValidationError("Due date cannot be before start date")


