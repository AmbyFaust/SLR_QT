import os

from qgis.gui import QgsMapCanvas, QgsMapToolPan
from qgis.core import QgsApplication, QgsRasterLayer


class MapCanvas(QgsMapCanvas):
    def __init__(self, parent=None):
        super(MapCanvas, self).__init__(parent)

        self.layer = QgsRasterLayer('IgnoreGetMapUrl=1&crs=EPSG:3857&dpiMode=7&format=image/png&layers=OGK1mln&styles=default&tileMatrixSet=urn:ogc:def:wkss:OGC:1.0:GoogleMapsCompatible&url=http://10.0.102.112:9419/GISWebServiceSE/service.php?request%3DGetCapabilities%26service%3DWMTS&username=user&password=12345678', 'OGK1mln', 'wms')

        self.setExtent(self.layer.extent())
        self.setLayers([self.layer])

        self.zoomToFullExtent()
        self._pan_tool = QgsMapToolPan(self)
        self.setMapTool(self._pan_tool)


if __name__ == '__main__':
    default_qgis_path = '/usr'
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if conda_prefix is not None:
        default_qgis_path = conda_prefix
        import platform
        if platform.system() == 'Windows':
            default_qgis_path = os.path.join(default_qgis_path, 'Library')
    qgs = QgsApplication([], True)
    qgs.setPrefixPath(os.environ.get('QGISPATH', default_qgis_path), True)
    qgs.initQgis()

    view = MapCanvas()
    view.show()

    qgs.setStyle("fusion")

    qgs.exec_()
    qgs.exitQgis()
