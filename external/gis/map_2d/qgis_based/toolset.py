from .map_canvas import MapCanvas
from .map_canvas_painter import MapCanvasPainter
from .maps.maps_manager import MapsManager

from typing import Optional


class MapQgsToolset:

    def __init__(self,  project_config_dir_path: str,
                 maps_config_path: Optional[str] = None,
                 maps_visibility_cache: Optional[str] = None):

        # создание объектов
        self.maps_manager = MapsManager(project_config_dir_path,
                                        config_path=maps_config_path, config_visibility_path=maps_visibility_cache)
        self.canvas = MapCanvas()
        self.painter = MapCanvasPainter(self.canvas, self.maps_manager)
        # обновление карт
        self.painter.visible_maps_changed_slot()

