from PyQt5.QtGui import QCursor, QPixmap

from qgis.core import QgsWkbTypes, QgsGeometry, QgsPointXY
from qgis.gui import QgsRubberBand

from .relocation_tool_base import RelocationToolBase

from ..map_canvas_painter import MapCanvasPainter
from ..objects.map_simple_objects import MapPoint
from ..coordinate_transformer import transformer


class MapPointRelocationTool(RelocationToolBase):

    # эмпирически подобранная константа (размер картинки при перетаскивании = размер картинки * этот множитель)
    IMAGE_SCALE_FACTOR = 4

    def __init__(self, painter: MapCanvasPainter, map_point: MapPoint):
        super().__init__(painter, map_point)
        self.cursor_image_mode = False
        self.point_rubber_band = QgsRubberBand(self.painter.canvas, QgsWkbTypes.PointGeometry)
        self.point_rubber_band.hide()

    def _start_actions(self):
        self.map_object.set_visibility(False)
        size = self.map_object.style.size * self.IMAGE_SCALE_FACTOR
        if self.map_object.style.image is not None:
            self.cursor_image_mode = True
            pixmap = QPixmap(self.map_object.style.image).scaled(size, size)
            self.setCursor(QCursor(pixmap))
        else:
            self.cursor_image_mode = False
            self.point_rubber_band.setStrokeColor(self.map_object.style.color)
            self.point_rubber_band.setWidth(size)
            point = transformer.lat_lon_to_map_xy(lat=self.map_object.latitude, lon=self.map_object.longitude)
            self.point_rubber_band.setToGeometry(QgsGeometry.fromPointXY(point), None)
            self.point_rubber_band.show()

    def _drop_actions(self):
        self.point_rubber_band.hide()
        self.map_object.set_visibility(True)

    def _finish_actions(self) -> object:
        self.map_object.latitude = self.finished_pos[0]
        self.map_object.longitude = self.finished_pos[1]
        self.map_object.redraw()
        return self.finished_pos

    def canvasMoveEvent(self, e):
        if not self.cursor_image_mode:
            point = QgsPointXY(e.originalMapPoint().x(), e.originalMapPoint().y())
            self.point_rubber_band.setToGeometry(QgsGeometry.fromPointXY(point), None)
            self.point_rubber_band.show()

