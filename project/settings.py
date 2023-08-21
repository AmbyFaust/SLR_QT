import os

from utils import coordinates_translator


MAIN_RASTER_MAP_PATH = os.path.abspath('./map/world.mbtiles')

PROJECTION_EPSG = coordinates_translator.CoordinateSystemEpsg.world_mercator
GEODETIC_EPSG = coordinates_translator.CoordinateSystemEpsg.wgs_84


# инициализация QGIS
MINICONDA_PATH = os.environ.get('CONDA_PREFIX')
QGIS_PLUGINS = None
QGIS_PATH = os.environ.get('QGISPATH')
if QGIS_PATH is None:
    QGIS_PATH = MINICONDA_PATH

