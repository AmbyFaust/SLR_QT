import copy
from functools import partial

from PyQt5.QtCore import QObject, pyqtSignal

from external.gis.map_2d.qgis_based import MapsManagerBase, MapInfo, MapKind
from project.singletons import concur_manager, concur_waiter, journal


class MapsCacher(QObject):
    map_is_cached = pyqtSignal(str)

    def __init__(self):
        super(MapsCacher, self).__init__(None)
        self.is_active = False

    def is_caching(self) -> bool:
        return copy.copy(self.is_active)

    def cache_map(self, map_path: str):
        self.is_active = True

        journal.log(f'Производится кэширование подложки {map_path}, '
                    f'процесс может занять несколько минут ...', attr='warning')

        concur_manager.add_task(
            self.__create_layer, map_path
        ).add_callback(
            concur_waiter.get_callback(partial(self.__layer_creation_callback, map_path=map_path))
        )

    @staticmethod
    def __create_layer(map_path: str):
        info = MapInfo('cache_key', 'cache_name', map_path, MapKind.Raster, '', True, True)
        MapsManagerBase.make_layer(info)

    def __layer_creation_callback(self, ret, *, map_path: str):
        self.map_is_cached.emit(map_path)
        self.is_active = False
        journal.log(f'Кэширование подложки {map_path} завершено', attr='warning')


