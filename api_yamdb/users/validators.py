from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import exceptions


class UsernameRegexValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\Z'
    flags = 0


def username_me(value):
    if value == 'me':
        raise exceptions.ValidationError(
            'Имя пользователя "me" не разрешено.'
        )
    return value
