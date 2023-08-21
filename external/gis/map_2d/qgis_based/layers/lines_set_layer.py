from PyQt5 import QtCore
from PyQt5.QtGui import QColor

from qgis.core import (QgsFeature, QgsGeometry, QgsSymbol, QgsWkbTypes, QgsSingleSymbolRenderer)

from .layer_base import VectorLayerBase
from ..coordinate_transformer import transformer


# label_tuple: ([label], label_color) - настройка подписей для каждой линии в объекте (подписи будут одного цвета)
class LinesSetStyle:
    def __init__(self, *, color=QColor(QtCore.Qt.red), opacity=None, width=0.3, label_tuple=[]):
        self.color = color
        self.opacity = opacity
        self.width = width
        self.label_tuple = label_tuple


class LinesSetLayer(VectorLayerBase):

    def __init__(self, *args, **kwargs):
        super(LinesSetLayer, self).__init__(*args, **kwargs)

    def _check(self, lines: [[()]], set_style: LinesSetStyle) -> bool:
        if not lines:
            return False
        return len(set_style.label_tuple[0]) == len(lines)

    def _create_features(self, lines: [[()]], set_style: LinesSetStyle):
        lines_xy = []
        for line in lines:
            lines_xy.append([transformer.lat_lon_to_map_xy(lat=p[0], lon=p[1]) for p in line if len(p) == 2])

        symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
        symbol.setColor(set_style.color)
        symbol.setWidth(set_style.width)
        if set_style.opacity is not None:
            symbol.setOpacity(set_style.opacity)

        renderer = QgsSingleSymbolRenderer(symbol)
        self.setRenderer(renderer)

        features = []
        for i in range(len(lines_xy)):
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry().fromPolylineXY(lines_xy[i]))
            if set_style.label_tuple[0]:
                self._set_feature_label(feat, (set_style.label_tuple[0][i],
                                               set_style.label_tuple[1],
                                               set_style.color))
            features.append(feat)

        self.startEditing()
        self.addFeatures(features)
        self.commitChanges()
