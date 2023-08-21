from abc import abstractmethod
from functools import wraps
from typing import List


class DrawableObject:
    def __init__(self, data):
        self.special_data = data
        self.validity = False

    def is_valid(self) -> bool:
        return self.validity


def create_object_decorator(draw_func):
    @wraps(draw_func)
    def wrapper(self, draw_hidden: bool = False, data=None, *args, **kwargs) -> int:
        drawable_object = draw_func(self, data, *args, **kwargs)
        if drawable_object is None:
            return self.INVALID_ID
        if not drawable_object.is_valid():
            return self.INVALID_ID
        object_id = self._create_object(drawable_object, draw_hidden)
        self._object_created(object_id, draw_hidden)
        return object_id
    return wrapper


def default_key_generator(existing_keys: List[int]):
    return 1 if len(existing_keys) == 0 else (max(existing_keys) + 1)


class Painter:
    INVALID_ID = None

    def __init__(self, key_generator_func=None):
        self._objects_dict = {}              # {код: объект}
        self._objects_visibility_dict = {}   # {код: видимость объекта}
        self._key_generator = key_generator_func if key_generator_func is not None else default_key_generator

    # --------------------------------------- Методы для работы с объектами ---------------------------------------
    def set_object_visibility(self, object_id, visibility):
        if object_id in self._objects_dict.keys():
            self._objects_visibility_dict[object_id] = visibility
            self._set_object_visibility(object_id, visibility)

    def remove_object(self, object_id: int):
        if object_id in self._objects_dict.keys():
            self._remove_object(object_id)
            self._objects_dict.pop(object_id)
            self._objects_visibility_dict.pop(object_id)

    # --------------------------------------------------------------------------------------------------------------
    @abstractmethod
    def _set_object_visibility(self, object_id, visibility):
        pass

    @abstractmethod
    def _remove_object(self, object_id):
        pass

    @abstractmethod
    def _object_created(self, object_id, draw_hidden):
        pass
    # --------------------------------------------------------------------------------------------------------------

    def _create_object(self, drawable_object: DrawableObject, draw_hidden: bool) -> int:
        object_id = self._key_generator(list(self._objects_dict.keys()))
        self._objects_dict[object_id] = drawable_object
        self._objects_visibility_dict[object_id] = not draw_hidden
        return object_id

    # --------------------------------------------------------------------------------------------------------------




