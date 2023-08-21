from external.gis.map_2d.qgis_based.map_canvas import MapCanvas

from .crs import canvas_crs


class CanvasWidget(MapCanvas):

    def __init__(self, parent=None):
        super(CanvasWidget, self).__init__(parent)
        self.setDestinationCrs(canvas_crs)


