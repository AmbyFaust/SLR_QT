from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from qgis.gui import QgsMapTool

from ..map_canvas import MapCanvas
from ..coordinate_transformer import transformer


class PositionTool(QgsMapTool):
    finished = pyqtSignal(float, float)  # широта, долгота

    def __init__(self, canvas: MapCanvas):
        super(PositionTool, self).__init__(canvas)
        self.map_canvas = canvas

    def start(self):
        self.map_canvas.setMapTool(self)

    def canvasPressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.map_canvas.use_default_tool()
            self.finished.emit(*transformer.x_y_to_lat_lon(x=e.originalMapPoint().x(), y=e.originalMapPoint().y()))


