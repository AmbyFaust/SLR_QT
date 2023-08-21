from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from .tool_base import ToolBase

from ..canvas_painter import CanvasPainter
from ..canvas_transformer import canvas_transformer
from ..canvas_target_point import CanvasTargetPoint


class TargetsPointsTool(ToolBase):
    tool_finished = pyqtSignal(list)  # [широта, долгота]

    def __init__(self, painter: CanvasPainter):
        super(TargetsPointsTool, self).__init__(painter)
        self.painter = painter
        self.points = []
        self.first_point_num = 0

    def start(self, first_point_num: int = None):
        if first_point_num is not None and first_point_num >= 0:
            self.first_point_num = first_point_num
        self.painter.canvas.setMapTool(self)

    def canvasPressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            lat, lon = canvas_transformer.x_y_to_lat_lon(x=e.originalMapPoint().x(), y=e.originalMapPoint().y())
            # создание и отрисовка отображаемой точки
            point = CanvasTargetPoint(len(self.points) + self.first_point_num, lat, lon, self.painter)
            point.draw()
            # добавление отображаемой точки в список
            self.points.append(point)
        if e.button() == QtCore.Qt.RightButton:
            pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:  # отмена всего
            for p in self.points:
                p.remove()
            self.points.clear()
            self.painter.canvas.use_default_tool()
            self.cancelled.emit()

        if e.key() == QtCore.Qt.Key_Backspace:  # удаление последней точки
            points_count = len(self.points)
            if points_count > 0:
                last_point = self.points[-1]
                last_point.remove()
                self.points.pop(points_count - 1)

        if e.key() == QtCore.Qt.Key_W:
            result = []
            # удаление точек со сцены и испускание сигнала с точками
            for p in self.points:
                p.remove()
                result.append((p.latitude, p.longitude, p.point_num))
            self.points.clear()
            self.tool_finished.emit(result)
            self.painter.canvas.use_default_tool()


