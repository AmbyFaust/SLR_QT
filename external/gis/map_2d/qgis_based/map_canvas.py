from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QDropEvent

from qgis.gui import (QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom)
from qgis.core import (QgsApplication, QgsNetworkAccessManager)

from .coordinate_transformer import transformer

import json


class MapCanvas(QgsMapCanvas):
    dropped = pyqtSignal(dict, float, float)  # mime_data_dict, lat, lon

    def __init__(self, parent=None):
        super(MapCanvas, self).__init__(parent)
        QgsNetworkAccessManager.instance().sslErrors.connect(lambda reply, _: reply.ignoreSslErrors())

        self.visible_maps = None

        self.__create_map_tools()
        self.use_default_tool()

        self.__tune_context_menu()

        self.setMouseTracking(True)
        self.enableAntiAliasing(True)

    def original_state(self):
        if self.visible_maps:
            self.setExtent(self.visible_maps[-1].extent())
        self.zoomToFullExtent()
        self.refresh()

    def center_to_point(self, latitude, longitude):
        self.zoomByFactor(1, transformer.lat_lon_to_map_xy(lat=latitude, lon=longitude))

    def use_default_tool(self):
        self.use_pan_tool()

    def use_increase_scale_tool(self):
        self.setMapTool(self.increase_scale_tool)

    def user_decrease_scale_tool(self):
        self.setMapTool(self.decrease_scale_tool)

    def use_pan_tool(self):
        self.setMapTool(self.pan_tool)

    def __create_map_tools(self):
        self.pan_tool = QgsMapToolPan(self)
        self.increase_scale_tool = QgsMapToolZoom(self, False)
        self.decrease_scale_tool = QgsMapToolZoom(self, True)

    def __tune_context_menu(self):
        self.contextMenuAboutToShow.connect(lambda menu, event: menu.clear())

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasText():
            pos_x_y = self.getCoordinateTransform().toMapCoordinates(event.pos())
            self.dropped.emit(json.loads(event.mimeData().text()),
                              *transformer.x_y_to_lat_lon(x=pos_x_y.x(), y=pos_x_y.y())
                              )
        event.accept()


if __name__ == '__main__':
    import os

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
