from PyQt5.QtCore import QObject

from project.gui.gis import CanvasPainter

from .canvas_mark import CanvasMark


class MarksHandler(QObject):

    def __init__(self, painter: CanvasPainter, parent=None):
        super().__init__(parent)
        self.painter = painter

    def test_draw(self):
        mark = CanvasMark(0, 0, self.painter)
        mark.draw(draw_hidden=False)




