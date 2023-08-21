from qgis.core import QgsRasterPipe, QgsRasterLayer, QgsRasterFileWriter


def write_raster_to_file(layer: QgsRasterLayer, file_path: str, writing_extent=None) -> bool:
    pipe = QgsRasterPipe()
    provider = layer.dataProvider()
    if not pipe.set(provider.clone()):
        return False
    extent = writing_extent if writing_extent is not None else layer.extent()
    file_writer = QgsRasterFileWriter(file_path)
    file_writer.writeRaster(pipe, provider.xSize(), provider.ySize(), extent, provider.crs())
    return True
