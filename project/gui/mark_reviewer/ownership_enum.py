from enum import Enum


class Ownership(Enum):
    FAMILIAR = 1
    UNFAMILIAR = 2
    UNKNOWN = 3


def int_to_ownership_type(val):
    if val == 1:
        return 'Свой'
    elif val == 2:
        return 'Чужой'
    else:
        return 'Неизвестно'


def ownership_type_to_int(val):
    if val == 'Свой':
        return 1
    elif val == 'Чужой':
        return 2
    else:
        return 3

