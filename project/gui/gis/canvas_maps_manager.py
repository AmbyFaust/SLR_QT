from typing import List

from PyQt5.QtCore import pyqtSignal


from external.gis.map_2d.qgis_based import MapsManagerBase, MapInfo, MapKind

from .crs import map_fragment_crs, set_layer_crs


class CanvasMapsManager(MapsManagerBase):
    maps_visibility_changed = pyqtSignal()

    MAIN_MAP_NAME = 'MAIN_MAP'
    MAIN_MAP_KEY = 'index_MAIN_MAP'

    def __init__(self, parent=None):
        super(CanvasMapsManager, self).__init__(parent)
        self.maps = {}
        self.visibilities = {}

    def update_layers(self, layers: List[MapInfo]):
        """
        Не закладывается функционал по добавлению новых подложек
        """
        pass

    def add_main_map(self, map_path: str, visibility=True):
        self.add_raster_fragment(
            self.MAIN_MAP_KEY, self.MAIN_MAP_NAME, map_path, visibility
        )

    def set_main_map_visibility(self, visibility: bool = True):
        self.set_raster_fragment_visibility(self.MAIN_MAP_KEY, visibility)

    def add_raster_fragment(self, fragment_key: str, fragment_name: str, fragment_path: str, visibility: bool):
        if fragment_key not in self.maps:
            raster_fragment = self.make_layer(
                MapInfo(fragment_key, fragment_name, fragment_path, MapKind.Raster, '', True, visibility)
            )
            # если вдруг отображаемая большая подложка не в СК солвера (СК отображения)
            if fragment_key is not self.MAIN_MAP_KEY:
                set_layer_crs(raster_fragment, map_fragment_crs)
            # -------------------------------------------------------------------------
            self.maps[fragment_key] = raster_fragment
            self.visibilities[fragment_key] = visibility
        self.maps_visibility_changed.emit()

    def set_raster_fragment_visibility(self, fragment_key: str, visibility: bool):
        if fragment_key not in self.maps or fragment_key not in self.visibilities:
            return
        self.visibilities[fragment_key] = visibility
        self.maps_visibility_changed.emit()

    def remove_raster_fragment(self, fragment_key: str):
        if fragment_key in self.maps:
            self.maps.pop(fragment_key)
        if fragment_key in self.visibilities:
            self.visibilities.pop(fragment_key)
        self.maps_visibility_changed.emit()

    def visible_layers(self) -> list:
        layers = [m for key, m in self.maps.items() if self.visibilities[key] is True and key != self.MAIN_MAP_KEY]
        if self.MAIN_MAP_KEY in self.maps and self.MAIN_MAP_KEY in self.visibilities:
            if self.visibilities[self.MAIN_MAP_KEY] is True:
                layers.append(self.maps[self.MAIN_MAP_KEY])  # подложка в самом нижнем слое
        return layers




