from PyQt5 import QtCore
from PyQt5.QtGui import QColor

from collections import namedtuple

from .selector_base import SelectorBase

from ..objects.map_simple_objects import MapPoint, PointStyle


map_point_selector_style = namedtuple('map_point_selector_style', ['svg_path', 'color'],
                                      defaults=[None, QColor(QtCore.Qt.black)])


class MapPointSelector(SelectorBase):

    def __init__(self, style: map_point_selector_style = None, *args, **kwargs):
        super(MapPointSelector, self).__init__(style, *args, **kwargs)
        self.map_frame = None

    def _get_default_settings(self):
        return map_point_selector_style()

    def _select(self):
        if self.map_frame is not None:
            self.map_frame.remove()

        # рисуется слой "точка" с картинкой
        if self.selector_settings.svg_path is not None:
            frame_style = PointStyle(size=self.map_object.style.size + 1, image=self.selector_settings.svg_path)
        # точка становится жирнее
        else:
            frame_style = PointStyle(size=self.map_object.style.size + 3, color=self.selector_settings.color)

        self.map_frame = MapPoint(self.map_object.latitude, self.map_object.longitude, frame_style, self.painter)
        self.map_frame.draw(draw_hidden=False)

    def _unselect(self):
        if self.map_frame is not None:
            self.map_frame.remove()
        self.map_frame = None

