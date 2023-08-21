from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from qgis.gui import QgsMapTool

from abc import abstractmethod

from ..map_canvas_painter import MapCanvasPainter
from ..coordinate_transformer import transformer


class RelocationToolBase(QgsMapTool):
    finished = pyqtSignal(object)

    def __init__(self, painter: MapCanvasPainter, map_object):
        super(RelocationToolBase, self).__init__(painter.canvas)
        self.painter = painter
        self.map_object = map_object
        self.finished_pos = None

    def start(self):
        self.painter.canvas.setMapTool(self)
        self._start_actions()

    def drop(self):
        self._drop_actions()
        self.painter.canvas.use_default_tool()

    def finish(self):
        self.drop()
        self.finished.emit(self._finish_actions())

    @abstractmethod
    def _start_actions(self):
        pass

    @abstractmethod
    def _finish_actions(self) -> object:
        pass

    @abstractmethod
    def _drop_actions(self):
        pass

    @abstractmethod
    def canvasMoveEvent(self, e):
        pass

    def canvasReleaseEvent(self, e):
        if e.button() == QtCore.Qt.RightButton:
            self.finished_pos = transformer.x_y_to_lat_lon(x=e.originalMapPoint().x(), y=e.originalMapPoint().y())
            self.finish()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.drop()






