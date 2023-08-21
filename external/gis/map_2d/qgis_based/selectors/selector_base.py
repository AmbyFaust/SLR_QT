from abc import ABC, abstractmethod

from ..map_canvas_painter import MapCanvasPainter


class SelectorBase(ABC):

    def __init__(self, selector_settings=None, *, painter: MapCanvasPainter):
        if selector_settings is None:
            self.selector_settings = self._get_default_settings()
        else:
            self.selector_settings = selector_settings
        self.painter = painter
        self.map_object = None
        self.map_object_meta = None
        self.is_active = False

    def set_map_object(self, map_object, *, meta=None):
        if self.is_active and self.map_object is not None:
            self.deactivate()
        self.map_object = map_object
        self.map_object_meta = meta
        self.is_active = False

    def get_map_object_meta(self):
        return self.map_object_meta

    def activate(self):
        if not self.is_active:
            if self.map_object is not None:
                self._select()
                self.is_active = True

    def deactivate(self):
        if self.is_active:
            if self.map_object is not None:
                self._unselect()
                self.is_active = False

    @abstractmethod
    def _get_default_settings(self):
        pass

    @abstractmethod
    def _select(self):
        pass

    @abstractmethod
    def _unselect(self):
        pass
