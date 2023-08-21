from PyQt5 import QtCore
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor, QPolygonF
from PyQt5.QtWidgets import QGraphicsTextItem

from qgis.core import QgsWkbTypes, QgsGeometry
from qgis.gui import QgsMapTool, QgsRubberBand

from ..coordinate_transformer import transformer

from ..objects.map_simple_objects import MapPoint, PointStyle
from ..objects.map_object_base import MapCanvasPainter, SpecialData

from geopy.distance import geodesic


def event_point_to_lat_lon(point):
    return transformer.x_y_to_lat_lon(x=point.x(), y=point.y())


class RulerTool(QgsMapTool):
    def __init__(self, painter: MapCanvasPainter, *, color=QColor(QtCore.Qt.darkMagenta), width=1):
        super(RulerTool, self).__init__(painter.canvas)
        self.color = color
        self.width = width

        self.painter = painter
        self.points = []

        self.rubber_band = QgsRubberBand(self.painter.canvas, QgsWkbTypes.LineGeometry)
        self.rubber_band.setStrokeColor(color)
        self.rubber_band.setWidth(width)
        self.rubber_band.hide()

        self.text_item = None

    def start(self):
        self.drop()
        self.painter.canvas.setMapTool(self)

    def finish(self):
        if len(self.points) < 2:
            self.drop()
        if len(self.points) >= 2:
            distance = self.__calc_distance((self.points[-1].latitude, self.points[-1].longitude))
            self.points[-1].style = PointStyle(color=self.color, label='{:.3f} м'.format(distance))
            self.points[-1].redraw()
            self.text_item.setPlainText('')
            self.__update_rubber_band()
            self.rubber_band.show()
        self.painter.canvas.use_default_tool()

    def drop(self):
        self.rubber_band.reset()
        if self.text_item is not None:
            self.text_item.setPlainText('')
        for p in self.points:
            p.remove()
        self.points.clear()
        self.painter.canvas.use_default_tool()

    def canvasPressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            lat, lon = event_point_to_lat_lon(e.originalMapPoint())
            m_point = MapPoint(lat, lon, PointStyle(color=self.color), self.painter, SpecialData(is_definable=False))
            m_point.draw()
            self.points.append(m_point)

    def canvasMoveEvent(self, e):
        if not self.points:
            return
        self.__update_rubber_band((e.originalMapPoint().x(), e.originalMapPoint().y()))
        self.rubber_band.show()

        if self.text_item is None:
            self.text_item = self.painter.canvas.scene().addText("Simple Test")
            assert isinstance(self.text_item, QGraphicsTextItem)
            self.text_item.setDefaultTextColor(self.color)

        distance = self.__calc_distance(transformer.x_y_to_lat_lon(x=e.originalMapPoint().x(),
                                                                   y=e.originalMapPoint().y()))
        self.text_item.setPlainText('{:.3f} м'.format(distance))
        self.text_item.setPos(self.painter.canvas.mapToScene(e.pos()))

    def canvasReleaseEvent(self, e):
        if e.button() == QtCore.Qt.RightButton:
            self.finish()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.drop()

    def __calc_distance(self, last_point):
        li = [(p.latitude, p.longitude) for p in self.points]
        li.append(last_point)
        return geodesic(*li).m

    def __update_rubber_band(self, last_xy_tup=None):
        poly = QPolygonF([QPointF(*transformer.lat_lon_to_map_xy(lat=p.latitude, lon=p.longitude)) for p in self.points])
        if last_xy_tup is not None:
            poly.append(QPointF(last_xy_tup[0], last_xy_tup[1]))
        self.rubber_band.setToGeometry(QgsGeometry.fromPolylineXY(QgsGeometry.createPolylineFromQPolygonF(poly)), None)













