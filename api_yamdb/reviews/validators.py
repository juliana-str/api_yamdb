import datetime
import re

from django.core.exceptions import ValidationError

REGEX_USERNAME = re.compile(r'^[\w.@+-]+')


def validate_username(value):
    if value == 'me':
        raise ValidationError('Использовать имя "me" запрещено!')
    if not REGEX_USERNAME.fullmatch(value):
        raise ValidationError(
            'Можно использовать только буквы, цифры и символы @.+-_".')


def validate_year(value):
    date = datetime.datetime.now().strftime("%Y")
    if value > int(date):
        raise ValidationError('Произведение еще не вышло!')
    return value
