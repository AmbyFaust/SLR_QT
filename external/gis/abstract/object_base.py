from abc import abstractmethod, ABC


class ObjectBase(ABC):
    def __init__(self, style, painter, special_data=None):
        self.style = style
        self.special_data = special_data
        self._painter = painter
        self._key = None
        self._visibility = None

    def draw(self, draw_hidden=False):
        if self._key is not None:
            return
        self._visibility = not draw_hidden
        self._key = self.sub_draw(draw_hidden)

    def set_visibility(self, visibility):
        if self._key is None:
            return
        self._painter.set_object_visibility(self._key, visibility)
        self._visibility = visibility

    def remove(self):
        if self._key is not None:
            self._painter.remove_object(self._key)
            self._key = None
            self._visibility = None

    def redraw(self):
        visibility = self._visibility
        self.remove()  # тут происходит сброс видимости
        self._visibility = visibility
        self.draw(not visibility)  # при перерисовке объекта сохраняем его текущую видимость

    def is_visible(self):
        return self._visibility

    @abstractmethod
    def sub_draw(self, draw_hidden) -> int:
        pass
