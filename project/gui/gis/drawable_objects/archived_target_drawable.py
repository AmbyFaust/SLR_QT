from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor

from external.gis.map_2d.qgis_based import MapPoint, PointStyle

from project.gui.generated import resources


class ArchivedTargetDrawable(MapPoint):
    """
    Класс для управления отрисовкой точек-целей из архива целей
    """
    DEFAULT_POINT_COLOR = QColor(Qt.darkYellow)
    POINT_SIZE = 4

    def __init__(self, point_num: int, latitude: float, longitude: float, painter,
                 *, type_name: str = None, color: QColor = None):
        self.point_num = point_num
        self.type_name = type_name
        style = PointStyle(
            color=color if color is not None else self.DEFAULT_POINT_COLOR,
            size=self.POINT_SIZE,
            label=f'Цель {point_num}' if type_name is None else f'Цель {point_num} [{type_name}]',
            image=':/images/cross.svg'
        )
        super(ArchivedTargetDrawable, self).__init__(latitude, longitude, style, painter)

