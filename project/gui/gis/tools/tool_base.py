from PyQt5.QtCore import pyqtSignal

from qgis.gui import QgsMapTool

from external.gis.map_2d.qgis_based import MapCanvasPainter


class ToolBase(QgsMapTool):

    cancelled = pyqtSignal()

    def __init__(self, painter: MapCanvasPainter):
        super(ToolBase, self).__init__(painter.canvas)
