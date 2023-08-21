from PyQt5 import QtCore
from PyQt5.QtGui import QColor

from qgis.core import (QgsFeature, QgsGeometry, QgsSymbol, QgsWkbTypes, QgsSingleSymbolRenderer,
                       QgsSvgMarkerSymbolLayer, QgsRuleBasedRenderer)

from .layer_base import VectorLayerBase
from ..coordinate_transformer import transformer


# label_tuple: ([label], label_color) - настройка подписей для каждой точки в объекте (подписи будут одного цвета)
class PointsSetStyle:
    def __init__(self, *, color=QColor(QtCore.Qt.red), opacity=None, size=2, label_tuple=[], image=None):
        self.color = color
        self.opacity = opacity
        self.size = size
        self.label_tuple = label_tuple
        self.image = image


class PointsSetLayer(VectorLayerBase):

    def __init__(self, *args, **kwargs):
        super(PointsSetLayer, self).__init__(*args, **kwargs)

    def _check(self, points: [()], set_style: PointsSetStyle) -> bool:
        if not points:
            return False
        return len(set_style.label_tuple[0]) == len(points)

    def _create_features(self, points: [()], set_style: PointsSetStyle):
        points_xy = [transformer.lat_lon_to_map_xy(lat=p[0], lon=p[1]) for p in points if len(p) == 2]

        if set_style.image is not None:
            symbol_layer = QgsSvgMarkerSymbolLayer(set_style.image, set_style.size)
            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
            symbol.changeSymbolLayer(0, symbol_layer)
            renderer = QgsRuleBasedRenderer(QgsSymbol.defaultSymbol(self.geometryType()))
            rule = QgsRuleBasedRenderer.Rule(symbol)
            renderer.rootRule().appendChild(rule)
            renderer.rootRule().removeChildAt(0)
        else:
            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
            symbol.setColor(set_style.color)
            symbol.setSize(set_style.size)
            if set_style.opacity is not None:
                symbol.setOpacity(set_style.opacity)
            renderer = QgsSingleSymbolRenderer(symbol)

        self.setRenderer(renderer)

        features = []
        for i in range(len(points_xy)):
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromPointXY(points_xy[i]))
            if set_style.label_tuple[0]:
                self._set_feature_label(feat, (set_style.label_tuple[0][i],
                                               set_style.label_tuple[1],
                                               set_style.color))
            features.append(feat)

        self.startEditing()
        self.addFeatures(features)
        self.commitChanges()
