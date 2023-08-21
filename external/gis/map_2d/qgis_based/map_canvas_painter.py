from PyQt5.QtCore import QObject, pyqtSignal

from enum import Enum

from typing import List, Tuple

from ...abstract import Painter, create_object_decorator

from .map_canvas import MapCanvas
from .maps.maps_manager import MapsManager

from .layers.layer_base import SpecialData
from .layers.point_layer import PointLayer, PointStyle
from .layers.line_layer import LineLayer, LineStyle
from .layers.polygon_layer import PolygonLayer, PolygonStyle
from .layers.points_set_layer import PointsSetLayer, PointsSetStyle
from .layers.lines_set_layer import LinesSetLayer, LinesSetStyle
from .layers.raster_fragment import RasterFragment, RasterFragmentStyle

from .common import ProviderType, Extent, extent_from_rectangle

from .coordinate_transformer import transformer


class LayerType(Enum):
    POINT = 1
    LINE = 2
    LINES_SET = 3
    POINTS_SET = 4
    POLYGON = 5
    RASTER_FRAGMENT = 6


class MapCanvasPainter(QObject, Painter):
    identified_data_signal = pyqtSignal(object, object)  # [identified_object_data_t], reference_data

    INVALID_ID = None

    def __init__(self, canvas: MapCanvas, maps_manager: MapsManager):
        super(MapCanvasPainter, self).__init__(parent=None)
        self.canvas = canvas
        self.maps_manager = maps_manager

    # ------------------------------------ Слоты для работы с картами ---------------------------------------------

    def visible_maps_changed_slot(self) -> None:
        self.canvas.visible_maps = self.maps_manager.visible_layers()
        self._refresh_canvas()
        # self.canvas.original_state()

    # ------------------------------------ Слоты для работы с инструментами ---------------------------------------

    def broadcast_identified_data(self, identified_data: list, identify_reference_data) -> None:
        """
        Метод для пересылки идентифицированных объектов через экземпляр данного класса
        """
        self.identified_data_signal.emit(identified_data, identify_reference_data)

    # --------------------------------------- Методы для создания объектов ---------------------------------------

    def draw_point(self, *, data: SpecialData, draw_hidden=False, coordinates: Tuple, style: PointStyle) -> int:
        return self.__create_layer(draw_hidden, data, LayerType.POINT, coordinates, style)

    def draw_line(self, *, data: SpecialData, points: List[Tuple], style: LineStyle, draw_hidden=False) -> int:
        return self.__create_layer(draw_hidden, data, LayerType.LINE, points, style)

    def draw_points_set(self, *, data: SpecialData, points: List[Tuple], style: PointsSetStyle, draw_hidden=False) -> int:
        return self.__create_layer(draw_hidden, data, LayerType.POINTS_SET, points, style)

    def draw_lines_set(self, *, data: SpecialData, lines: List[List[Tuple]], style: LinesSetStyle, draw_hidden=False) -> int:
        return self.__create_layer(draw_hidden, data, LayerType.LINES_SET, lines, style)

    def draw_polygon(self, *, data: SpecialData, points: List[Tuple], style: PolygonStyle, draw_hidden=False) -> int:
        return self.__create_layer(draw_hidden, data, LayerType.POLYGON, points, style)

    def draw_raster_fragment(self, *, data: SpecialData, style: RasterFragmentStyle, draw_hidden=False) -> int:
        return self.__create_layer(draw_hidden, data, LayerType.RASTER_FRAGMENT, None, style)

    # ---------------------------------------- Методы для работы со слоями -----------------------------------------

    def zoom_to_object(self, object_id) -> None:
        if object_id not in self._objects_dict:
            return
        self.canvas.setExtent(self._objects_dict[object_id].extent())
        self.canvas.refresh()

    def get_object_center(self, object_id) -> tuple:
        if object_id not in self._objects_dict:
            return None
        layer_ext = self._objects_dict[object_id].extent()
        center = extent_from_rectangle(layer_ext).center()
        return transformer.x_y_to_lat_lon(x=center[0], y=center[1])

    def get_object_extent(self, object_id) -> Extent:
        if object_id not in self._objects_dict:
            return None
        return extent_from_rectangle(self._objects_dict[object_id].extent())

    # ---------------------------------------- Защищенные методы ---------------------------------------------------

    def _set_object_visibility(self, object_id, visibility):
        self._refresh_canvas()

    def _remove_object(self, object_id):
        layer = self._objects_dict[object_id]
        if layer in self.canvas.layers():
            self.canvas.layers().remove(layer)
            self.canvas.refresh()

    def _object_created(self, _, draw_hidden):
        if not draw_hidden:
            self._refresh_canvas()

    # -------------------------------------------- Приватные методы -------------------------------------------------

    @create_object_decorator
    def __create_layer(self, data, layer_type: LayerType, geometry, style):
        # растровый фрагмент
        if layer_type is LayerType.RASTER_FRAGMENT:
            if style.raster_data.provider is not ProviderType.none:
                fragment = RasterFragment(
                    data, style.raster_data.prepare_url(), style.raster_data.id, style.raster_data.provider.provider_str
                )
            else:
                fragment = RasterFragment(
                    data, style.raster_data.prepare_url(), style.raster_data.id
                )
            fragment.setup(style)
            return fragment
        # векторные слои
        if layer_type is LayerType.POINT:
            layer = PointLayer(data, 'Point', 'point', 'memory')
        elif layer_type is LayerType.POINTS_SET:
            layer = PointsSetLayer(data, 'Point', 'point', 'memory')
        elif layer_type is LayerType.LINE:
            layer = LineLayer(data, 'LineString', 'line', 'memory')
        elif layer_type is LayerType.LINES_SET:
            layer = LinesSetLayer(data, 'LineString', 'line', 'memory')
        elif layer_type is LayerType.POLYGON:
            layer = PolygonLayer(data, 'Polygon', 'polygon', 'memory')
        else:
            return None
        layer.setup(geometry, style)  # настройка слоя
        return layer

    def _refresh_canvas(self):
        visible_layers = []  # векторные объекты
        visible_fragments = []  # растровые объекты
        for layer_id, visibility in self._objects_visibility_dict.items():
            obj = self._objects_dict[layer_id]
            if isinstance(obj, RasterFragment):
                if visibility:
                    visible_fragments.append(obj)
            elif visibility:
                visible_layers.append(obj)

        if self.canvas.visible_maps is None or len(self.canvas.visible_maps) == 0:
            self.canvas.setLayers(visible_layers + visible_fragments)
        else:
            self.canvas.setLayers(visible_layers + visible_fragments + self.canvas.visible_maps)
    # -------------------------------------------------------------------------------------------------------------







