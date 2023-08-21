from abc import ABC
import typing

from ....abstract import ObjectBase
from ..map_canvas_painter import MapCanvasPainter, SpecialData, Extent


class MapObjectBase(ObjectBase, ABC):
    def __init__(self, style, painter: MapCanvasPainter, data: SpecialData = None):
        special_data = data if data is not None else SpecialData()
        super().__init__(style, painter, special_data)

    def zoom_to_object(self):
        if self._key is not None:
            self._painter.zoom_to_object(self._key)

    def get_object_center(self):
        if self._key is not None:
            return self._painter.get_object_center(self._key)
        return None

    def get_object_extent(self):
        if self._key is not None:
            return self._painter.get_object_extent(self._key)
        return None




