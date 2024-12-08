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


# def validate_password_strength(value): automatic validation is good enough.
#
#     if len(value) < 8:
#         raise ValidationError('Password must be at least 8 characters long.')
#
#     if not re.search(r'[A-Z]', value):
#         raise ValidationError('Password must contain at least one uppercase letter.')
#
#     if not re.search(r'[a-z]', value):
#         raise ValidationError('Password must contain at least one lowercase letter.')
#
#     if not re.search(r'\d', value):
#         raise ValidationError('Password must contain at least one number.')
#
#     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
#         raise ValidationError('Password must contain at least one special character.')