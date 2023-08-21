from typing import Tuple, List

from .map_object_base import MapObjectBase
from ..layers import PointStyle, LineStyle, PointsSetStyle, LinesSetStyle, PolygonStyle, RasterFragmentStyle


class MapPoint(MapObjectBase):
    def __init__(self, latitude, longitude, style: PointStyle, *args, **kwargs):
        super(MapPoint, self).__init__(style, *args, **kwargs)
        self.latitude = latitude
        self.longitude = longitude

    def sub_draw(self, draw_hidden):
        return self._painter.draw_point(data=self.special_data,
                                        coordinates=(self.latitude, self.longitude),
                                        style=self.style, draw_hidden=draw_hidden)


class MapPointsSet(MapObjectBase):
    def __init__(self, points: List[Tuple[float, float]], style: PointsSetStyle, *args, **kwargs):
        super(MapPointsSet, self).__init__(style, *args, **kwargs)
        self.points = points

    def sub_draw(self, draw_hidden):
        return self._painter.draw_points_set(data=self.special_data,
                                             points=self.points, style=self.style, draw_hidden=draw_hidden)


class MapLine(MapObjectBase):
    def __init__(self, points: List[Tuple[float, float]], style: LineStyle, *args, **kwargs):
        super(MapLine, self).__init__(style, *args, **kwargs)
        self.points = points

    def sub_draw(self, draw_hidden):
        return self._painter.draw_line(data=self.special_data,
                                       points=self.points, style=self.style, draw_hidden=draw_hidden)


class MapLinesSet(MapObjectBase):
    def __init__(self, lines: List[List[Tuple[float, float]]], style: LinesSetStyle, *args, **kwargs):
        super(MapLinesSet, self).__init__(style, *args, **kwargs)
        self.lines = lines

    def sub_draw(self, draw_hidden):
        return self._painter.draw_lines_set(data=self.special_data,
                                            lines=self.lines, style=self.style, draw_hidden=draw_hidden)


class MapPolygon(MapObjectBase):
    def __init__(self, points: List[Tuple[float, float]], style: PolygonStyle, *args, **kwargs):
        super(MapPolygon, self).__init__(style, *args, **kwargs)
        self.points = points

    def sub_draw(self, draw_hidden):
        return self._painter.draw_polygon(data=self.special_data,
                                          points=self.points, style=self.style, draw_hidden=draw_hidden)


class MapRasterFragment(MapObjectBase):
    def __init__(self, style: RasterFragmentStyle, *args, **kwargs):
        super(MapRasterFragment, self).__init__(style, *args, **kwargs)

    def sub_draw(self, draw_hidden) -> int:
        return self._painter.draw_raster_fragment(data=self.special_data,
                                                  style=self.style, draw_hidden=draw_hidden)
