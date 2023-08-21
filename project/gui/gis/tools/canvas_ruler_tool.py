from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from external.gis.map_2d.qgis_based import RulerTool


class CanvasRulerTool(RulerTool):
    cancelled = pyqtSignal()
    finished = pyqtSignal()
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.drop()
            self.cancelled.emit()
    
    def canvasReleaseEvent(self, e):
        if e.button() == QtCore.Qt.RightButton:
            self.finish()
            self.finished.emit()
    

