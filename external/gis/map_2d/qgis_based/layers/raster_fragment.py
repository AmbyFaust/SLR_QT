from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from qgis.core import QgsRasterFileWriter, QgsRasterPipe, QgsSingleBandColorDataRenderer, \
    QgsColorRampShader, QgsRasterShader, QgsSingleBandPseudoColorRenderer, QgsSingleBandColorDataRenderer

from .layer_base import RasterLayerBase

from ..common import RasterData


class RasterFragmentStyle:
    def __init__(self, *, opacity=0.1, raster_data: RasterData):
        self.opacity = opacity
        self.raster_data = raster_data


class RasterFragment(RasterLayerBase):
    def __init__(self, *args, **kwargs):
        super(RasterFragment, self).__init__(*args, **kwargs)

    def _setup(self, style: RasterFragmentStyle) -> bool:
        self.setOpacity(style.opacity)
        return True

    def _create_renderers(self):
        pass
        # fcn = QgsColorRampShader()
        # fcn.setColorRampType(QgsColorRampShader.Interpolated)
        # lst = [QgsColorRampShader.ColorRampItem(0, QColor(0, 0, 0)),
        #        QgsColorRampShader.ColorRampItem(255, QColor(255, 255, 255))]
        # fcn.setColorRampItemList(lst)
        # shader = QgsRasterShader()
        # shader.setRasterShaderFunction(fcn)
        #
        # renderer = QgsSingleBandPseudoColorRenderer(self.dataProvider(), 1, shader)
        # renderer.setAlphaBand(1)
        # self.setRenderer(renderer)




