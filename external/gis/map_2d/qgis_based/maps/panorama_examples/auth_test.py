import os

from PyQt5.QtWidgets import QWidget
from qgis.core import QgsRasterLayer
from qgis.core import QgsDataSourceUri
from qgis.core import QgsAuthMethodConfig
from qgis.core import QgsApplication


def create_test_wms_layer():
    auth_mgr = QgsApplication.authManager()

    config = QgsAuthMethodConfig("Basic")
    config.setName("LGP")
    config.setConfig("username", "user")
    config.setConfig("password", "12345678")
    assert (auth_mgr.storeAuthenticationConfig(config)[0])
    assert config.isValid()

    auth_mgr.storeAuthenticationConfig(config)
    new_auth_cfg_id = config.id()
    print(auth_mgr.authMethod("Basic").supportedDataProviders())
    assert new_auth_cfg_id

    quri = QgsDataSourceUri()
    quri.setParam("crs", "EPSG:3395")
    quri.setParam("dpiMode", "7")
    quri.setParam("format", "image/png")
    quri.setParam("layers", "0001")
    quri.setParam("styles", "")
    quri.setParam("url", "https//10.0.102.112:9419/GISWebServiceSE/service.php")
    quri.setParam("authcfg", new_auth_cfg_id)
    print(str(quri.encodedUri(), "utf-8"))
    rlayer = QgsRasterLayer(str(quri.encodedUri(), "utf-8"), 'OGK1mln', 'wms')

    assert rlayer.isValid()
    return rlayer


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
    # windows_conda_qgis_path = 'C:/Polygon/miniconda3/envs/gui_input_system/Library'
    # qgs.setPrefixPath(os.environ.get('QGISPATH', windows_conda_qgis_path), True)
    qgs.initQgis()

    create_test_wms_layer()

    main_window = QWidget()
    main_window.show()

    qgs.setStyle("fusion")

    qgs.exec_()
    qgs.exitQgis()
