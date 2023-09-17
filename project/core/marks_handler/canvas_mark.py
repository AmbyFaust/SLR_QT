from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from external.gis.map_2d.qgis_based import MapPoint, PointStyle

from project.gui.generated import resources


class CanvasMark(MapPoint):
    """
    Класс для управления отрисовкой отметок
    """
    POINT_COLOR = QColor(Qt.red)
    POINT_SIZE = 4

    def __init__(self, map_mark_id: int, mark_name: str, latitude: float, longitude: float, painter):
        self.id = map_mark_id
        self.mark_name = mark_name
        style = PointStyle(
            color=self.POINT_COLOR,
            size=self.POINT_SIZE,
            label=f'Отметка {self.mark_name}',
            #image=':/images/cross.svg'
            image=''
        )
        super(CanvasMark, self).__init__(latitude, longitude, style, painter)

    def redraw(self):
        self.style.label = f'Отметка {self.mark_name}'
        super(CanvasMark, self).redraw()


