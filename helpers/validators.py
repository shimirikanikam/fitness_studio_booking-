import re

from helpers import message_codes
from rest_framework import serializers


def validate_alphabetic_only(field_name):
    def validator(value):
        pattern = r"^[A-Za-z\s]+$"
        if not re.match(pattern, value):
            message = message_codes.UMI_4003_ALPHABETIC_ONLY_ERROR_MESSAGE
            code = message_codes.UMI_4003_ALPHABETIC_ONLY_ERROR_CODE
            raise serializers.ValidationError(message.format(field_name),
                                              code=code)
    return validator



