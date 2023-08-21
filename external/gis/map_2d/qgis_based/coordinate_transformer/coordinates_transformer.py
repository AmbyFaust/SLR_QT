from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsPointXY

from .default_settings import default_geographic_epsg, default_projection_epsg

from .. import local_settings


class CoordinateTransformer:

    def __init__(self):
        if hasattr(local_settings, 'geographic_epsg'):
            self.geographic_srs = QgsCoordinateReferenceSystem(local_settings.geographic_epsg)
        else:
            self.geographic_srs = QgsCoordinateReferenceSystem(default_geographic_epsg)
        if hasattr(local_settings, 'projection_epsg'):
            self.projection_srs = QgsCoordinateReferenceSystem(local_settings.projection_epsg)
        else:
            self.projection_srs = QgsCoordinateReferenceSystem(default_projection_epsg)

    def lat_lon_to_map_xy(self, *, lat, lon) -> QgsPointXY:
        tr = QgsCoordinateTransform()
        tr.setSourceCrs(self.geographic_srs)
        tr.setDestinationCrs(self.projection_srs)
        return tr.transform(QgsPointXY(lon, lat))

    def x_y_to_lat_lon(self, *, x, y) -> 'latitude, longitude':
        tr = QgsCoordinateTransform()
        tr.setSourceCrs(self.projection_srs)
        tr.setDestinationCrs(self.geographic_srs)
        point = tr.transform(QgsPointXY(x, y))
        return point.y(), point.x()

    def get_geographic_srs_id(self) -> int:
        return self.geographic_srs.srsid()

    def get_projection_srs_id(self) -> int:
        return self.projection_srs.srsid()


transformer = CoordinateTransformer()
