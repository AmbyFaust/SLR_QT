from external.gis.map_2d.qgis_based import MapCanvasPainter
from external.gis.map_2d.qgis_based.map_canvas_painter import RasterFragment

from .crs import sar_crs, vector_crs, set_layer_crs


class CanvasPainter(MapCanvasPainter):

    def __init__(self, *args, **kwargs):
        super(CanvasPainter, self).__init__(*args, **kwargs)

    def remove_map(self, map_key):
        """
        Удаление фрагмента подложки
        """
        self.remove_object(map_key)

    def _refresh_canvas(self):
        visible_layers = []  # векторные объекты
        visible_images = []  # растровые объекты (РЛИ)
        for layer_id, visibility in self._objects_visibility_dict.items():
            obj = self._objects_dict[layer_id]
            if isinstance(obj, RasterFragment):
                if visibility:
                    set_layer_crs(obj, sar_crs)  # конвертация СК (на всякий случай)
                    visible_images.append(obj)
            elif visibility:
                set_layer_crs(obj, vector_crs)   # конвертация СК (на всякий случай)
                visible_layers.append(obj)

        if self.canvas.visible_maps is None or len(self.canvas.visible_maps) == 0:
            self.canvas.setLayers(visible_layers + visible_images)  # сначала векторы, потом растры
        else:
            # сначала векторы, потом растры, потом подложки (как векторные, так и растровые)
            self.canvas.setLayers(visible_layers + visible_images + self.canvas.visible_maps)
        
        self.canvas.refresh()


