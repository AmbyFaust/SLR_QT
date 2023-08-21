from collections import namedtuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from external.gis.map_2d.qgis_based import MapPointsSet, PointsSetStyle

from project.gui.generated import resources


history_target_data = namedtuple('HistoryTargetData',
                                 ['session_name', 'point_num', 'latitude', 'longitude', 'type_name'],
                                 defaults=['', None, None, None, None]
                                 )


class HistoryTargetsSet(MapPointsSet):

    DEFAULT_POINT_COLOR = QColor("#7AD176")
    POINT_SIZE = 4

    def __init__(self, targets: [history_target_data], painter, color: QColor = None):
        try:
            points, labels = [], []
            color = color if color is not None else self.DEFAULT_POINT_COLOR
            for tgt in targets:
                points.append((tgt.latitude, tgt.longitude))
                labels.append(self.create_label(tgt.session_name, tgt.point_num, tgt.type_name))

            style = PointsSetStyle(color=color, size=self.POINT_SIZE,
                                   label_tuple=(labels, color), image=':/images/cross.svg')
            super(HistoryTargetsSet, self).__init__(points, style, painter)

        except BaseException as exp:
            print(exp)

    @staticmethod
    def create_label(session_name: str, target_num: int, type_name: str=None) -> str:
        if type_name is not None:
            return f'[{session_name}]--Цель {target_num}--[{type_name}]'
        else:
            return f'[{session_name}]--Цель {target_num}'





