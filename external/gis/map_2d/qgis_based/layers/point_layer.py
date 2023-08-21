from PyQt5 import QtCore
from PyQt5.QtGui import QColor

from qgis.core import (QgsFeature, QgsGeometry, QgsSymbol, QgsWkbTypes, QgsSingleSymbolRenderer,
                       QgsSvgMarkerSymbolLayer, QgsRuleBasedRenderer)

from .layer_base import VectorLayerBase
from ..coordinate_transformer import transformer


class PointStyle:
    def __init__(self, *, color=QColor(QtCore.Qt.red), opacity=None, size=2, label=None, label_color=None, image=None):
        self.color = color
        self.opacity = opacity
        self.size = size
        self.label = label
        self.label_color = label_color
        self.image = image


class PointLayer(VectorLayerBase):

    def __init__(self, *args, **kwargs):
        super(PointLayer, self).__init__(*args, **kwargs)

    def _check(self, coordinates: (), *_) -> bool:
        return len(coordinates) == 2

    def _create_features(self, coordinates, point_style: PointStyle):
        point_xy = transformer.lat_lon_to_map_xy(lat=coordinates[0], lon=coordinates[1])

        if point_style.image is not None:
            symbol_layer = QgsSvgMarkerSymbolLayer(point_style.image, point_style.size)
            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
            symbol.changeSymbolLayer(0, symbol_layer)
            renderer = QgsRuleBasedRenderer(QgsSymbol.defaultSymbol(self.geometryType()))
            rule = QgsRuleBasedRenderer.Rule(symbol)
            renderer.rootRule().appendChild(rule)
            renderer.rootRule().removeChildAt(0)
        else:
            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
            symbol.setColor(point_style.color)
            symbol.setSize(point_style.size)
            if point_style.opacity is not None:
                symbol.setOpacity(point_style.opacity)
            renderer = QgsSingleSymbolRenderer(symbol)

        self.setRenderer(renderer)

        geom = QgsGeometry.fromPointXY(point_xy)
        geom.convertToSingleType()

        feat = QgsFeature()
        feat.setGeometry(geom)
        if point_style.label is not None:
            self._set_feature_label(feat, (point_style.label, point_style.label_color, point_style.color))

        self.startEditing()
        self.addFeature(feat)
        self.commitChanges()
