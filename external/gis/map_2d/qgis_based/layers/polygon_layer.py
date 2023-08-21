from PyQt5 import QtCore
from PyQt5.QtGui import QColor

from qgis.core import (QgsFeature, QgsGeometry, QgsSymbol, QgsWkbTypes, QgsSingleSymbolRenderer)

from .layer_base import VectorLayerBase
from ..coordinate_transformer import transformer


class PolygonStyle:
    def __init__(self, *, color=QColor(QtCore.Qt.red), opacity=0.1, label=None, label_color=None):
        self.color = color
        self.opacity = opacity
        self.label = label
        self.label_color = label_color


class PolygonLayer(VectorLayerBase):

    def __init__(self, *args, **kwargs):
        super(PolygonLayer, self).__init__(*args, **kwargs)

    def _check(self, points: [()], *_) -> bool:
        if not points:
            return False
        return len(points) > 0

    def _create_features(self, points: [()], polygon_style: PolygonStyle):
        qgs_points = [transformer.lat_lon_to_map_xy(lat=p[0], lon=p[1]) for p in points if len(p) == 2]

        symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PolygonGeometry)
        symbol.setColor(polygon_style.color)
        if polygon_style.opacity is not None:
            symbol.setOpacity(polygon_style.opacity)

        renderer = QgsSingleSymbolRenderer(symbol)
        self.setRenderer(renderer)

        feat = QgsFeature()
        feat.setGeometry(QgsGeometry().fromPolygonXY([qgs_points]))

        if polygon_style.label is not None:
            self._set_feature_label(feat, (polygon_style.label, polygon_style.label_color, polygon_style.color))

        self.startEditing()
        self.addFeature(feat)
        self.commitChanges()
