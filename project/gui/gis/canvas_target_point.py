from PyQt5.QtGui import QColor

from external.gis.map_2d.qgis_based import MapPoint, PointStyle

from project.gui.generated import resources


class CanvasTargetPoint(MapPoint):
    """
    Класс для управления отрисовкой точек-целей
    """
    POINT_COLOR = QColor("#7AD176")
    POINT_SIZE = 4

    def __init__(self, point_num: int, latitude: float, longitude: float, painter):
        self.point_num = point_num
        style = PointStyle(
            color=self.POINT_COLOR,
            size=self.POINT_SIZE,
            label=f'Цель {point_num}',
            image=':/images/cross.svg'
        )
        super(CanvasTargetPoint, self).__init__(latitude, longitude, style, painter)

