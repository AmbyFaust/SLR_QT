from PyQt5 import QtCore
from PyQt5.QtGui import QColor

from qgis.core import (QgsFeature, QgsGeometry, QgsSymbol, QgsWkbTypes, QgsSingleSymbolRenderer)

from .layer_base import VectorLayerBase
from ..coordinate_transformer import transformer


class LineStyle:
    def __init__(self, *, color=QColor(QtCore.Qt.blue), opacity=None, width=0.3, label=None, label_color=None):
        self.color = color
        self.opacity = opacity
        self.width = width
        self.label = label
        self.label_color = label_color


class LineLayer(VectorLayerBase):

    def __init__(self, *args, **kwargs):
        super(LineLayer, self).__init__(*args, **kwargs)

    def _check(self, points: [()], *_) -> bool:
        return len(points) > 1

    def _create_features(self, points: [()], line_style: LineStyle):
        line_xy = [transformer.lat_lon_to_map_xy(lat=p[0], lon=p[1]) for p in points if len(p) == 2]

        symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.LineGeometry)
        symbol.setColor(line_style.color)
        symbol.setWidth(line_style.width)
        if line_style.opacity is not None:
            symbol.setOpacity(line_style.opacity)

        renderer = QgsSingleSymbolRenderer(symbol)
        self.setRenderer(renderer)

        feat = QgsFeature()
        feat.setGeometry(QgsGeometry().fromPolylineXY(line_xy))
        if line_style.label is not None:
            self._set_feature_label(feat, (line_style.label, line_style.label_color, line_style.color))

        self.startEditing()
        self.addFeature(feat)
        self.commitChanges()
