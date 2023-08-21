from PyQt5 import QtCore
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QPolygonF

from qgis.core import QgsWkbTypes, QgsGeometry
from qgis.gui import QgsRubberBand

from collections import namedtuple

from .selector_base import SelectorBase

from ..objects.map_simple_objects import MapLine, LineStyle
from ..coordinate_transformer import transformer


map_line_selector_style = namedtuple('map_line_selector_style',
                                     ['line_color', 'line_opacity', 'selection_color', 'selection_width_factor'],
                                     defaults=[QColor(QtCore.Qt.darkGreen), 1, QColor(QtCore.Qt.yellow), 2]
                                     )


class MapLineSelector(SelectorBase):

    def __init__(self, style: map_line_selector_style = None, *args, **kwargs):
        super(MapLineSelector, self).__init__(style, *args, **kwargs)
        self.temp_map_line = None
        self.prev_opacity = None
        self.rubber_band = QgsRubberBand(self.painter.canvas, QgsWkbTypes.LineGeometry)
        self.rubber_band.hide()

    def _get_default_settings(self):
        return map_line_selector_style()

    def _select(self):
        # прячем линию маршрута
        self.__hide_route_line(True)
        # настройка и отрисовка временной линии маршрута
        if self.temp_map_line is not None:
            self.temp_map_line.remove()
        temp_style = LineStyle(color=self.selector_settings.line_color,
                               opacity=self.selector_settings.line_opacity,
                               width=self.map_object.style.width + 1,
                               label=None,
                               label_color=None
                               )
        self.temp_map_line = MapLine(self.map_object.points, temp_style, self.painter)
        self.temp_map_line.draw()
        # рисуем "резиновую рамку"
        self.rubber_band.setWidth((self.map_object.style.width + 1) * self.selector_settings.selection_width_factor)
        self.rubber_band.setStrokeColor(self.selector_settings.selection_color)
        poly = QPolygonF([QPointF(*transformer.lat_lon_to_map_xy(lat=p[0], lon=p[1])) for p in self.map_object.points])
        self.rubber_band.setToGeometry(QgsGeometry.fromPolylineXY(QgsGeometry.createPolylineFromQPolygonF(poly)), None)
        self.rubber_band.show()

    def _unselect(self):
        # показываем линию маршрута
        if self.temp_map_line is not None:
            self.temp_map_line.remove()
            self.temp_map_line = None
        self.__hide_route_line(False)
        # прячем "резиновую рамку"
        self.rubber_band.reset()
        self.rubber_band.hide()

    def __hide_route_line(self, hide_flag=True):
        if hide_flag:
            self.prev_opacity = self.map_object.style.opacity
            opacity = 0
        else:
            opacity = self.prev_opacity
        self.map_object.style = LineStyle(color=self.map_object.style.color,
                                          opacity=opacity,
                                          width=self.map_object.style.width,
                                          label=self.map_object.style.label,
                                          label_color=self.map_object.style.label_color
                                          )
        self.map_object.redraw()




