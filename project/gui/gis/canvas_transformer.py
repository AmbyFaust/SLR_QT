from qgis.core import QgsCoordinateReferenceSystem

from external.gis.map_2d.qgis_based import transformer

from project.settings import PROJECTION_EPSG, GEODETIC_EPSG


# так как пакет ГИС не умеет настраивать используемые СК, сделаем это извне
canvas_transformer = transformer
canvas_transformer.geographic_srs = QgsCoordinateReferenceSystem(GEODETIC_EPSG.value)
canvas_transformer.projection_srs = QgsCoordinateReferenceSystem(PROJECTION_EPSG.value)



