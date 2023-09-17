import os

IMAGE_DIRECTORY = os.getcwd() + '/project/gui/mark_reviewer/resources/images/'
VISIBILITY_VARIANTS = 2

_OBJECTS_CLASSIFIER = {
    "0": ["Нет данных", "Не определено"],
    "1": ["Объект", "Настоящий объект"],
    "2": ["Чел", "Человек"]
}

_REVERSE_OBJECTS_CLASSIFIER = {', '.join(value): key for key, value in _OBJECTS_CLASSIFIER.items()}


