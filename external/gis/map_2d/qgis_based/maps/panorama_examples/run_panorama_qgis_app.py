import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QDockWidget
from qgis.gui import QgsMapCanvas, QgsMapToolPan
from qgis.core import QgsApplication

from vp.gui.gis.misc.layers_widget import LayersWidget
from vp.gui.gis.misc.maps_manager import MapsManager


class MapCanvas(QgsMapCanvas):
    def __init__(self, parent=None):
        super(MapCanvas, self).__init__(parent)

        self.maps_manager = MapsManager()
        visible_layers = self.maps_manager.visible_maps()
        if visible_layers:
            self.setExtent(visible_layers[-1].extent())

        self.setLayers(visible_layers)

        # Тестовая карта Ногинска
        # url_with_params = \
        #     "crs=EPSG:3395&dpiMode=7&format=image/png&layers=0001&styles=&url=http://10.0.102.112:9418/GISWebServiceSE/service.php&username=user&password=12345678"

        self.zoomToFullExtent()
        self._pan_tool = QgsMapToolPan(self)
        self.setMapTool(self._pan_tool)

    def show_visible_layers(self):
        visible_layers = self.maps_manager.visible_maps()
        self.setLayers(visible_layers)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Тестовое отображение 2D карт от сервера "Панорама"')

        self.canvas = MapCanvas()
        self.setCentralWidget(self.canvas)

        self.layers_dock = QDockWidget("Слои 2D карты")
        self.layers_widget = LayersWidget(self.canvas.maps_manager.maps_data)
        self.layers_dock.setWidget(self.layers_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.layers_dock)

        self.layers_widget.visible_layers_changed.connect(self.canvas.show_visible_layers)

    def closeEvent(self, event: QCloseEvent):
        self.canvas.maps_manager.maps_data.save()


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
    # print(default_qgis_path)
    # windows_conda_qgis_path = 'C:/Polygon/miniconda3/envs/gui_input_system/Library'
    # qgs.setPrefixPath(os.environ.get('QGISPATH', windows_conda_qgis_path), True)
    qgs.initQgis()
    # listProvider = qgs.dataItemProviderRegistry().providers()
    # for provider in listProvider:
    #     print(provider.name(), provider.dataProviderKey())

    main_window = MainWindow()
    main_window.show()

    qgs.setStyle("fusion")

    qgs.exec_()
    qgs.exitQgis()
