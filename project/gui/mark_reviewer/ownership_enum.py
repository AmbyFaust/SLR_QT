from enum import Enum


class Ownership(Enum):
    FAMILIAR = (1, 'Неизвестно')
    UNFAMILIAR = (2, 'Свой')
    UNKNOWN = (3, 'Чужой')

    def __new__(cls, value, description):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def int_to_ownership_type(cls, value):
        for item in cls:
            if item.value == value:
                return item.description
        return None

    @classmethod
    def ownership_type_to_int(cls, ownership_name):
        for item in cls:
            if item.description == ownership_name:
                return item.value
        return None

