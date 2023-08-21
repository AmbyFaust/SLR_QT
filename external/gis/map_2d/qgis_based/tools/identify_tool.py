from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal

from collections import namedtuple

from ..map_canvas_painter import MapCanvasPainter

from qgis.gui import QgsMapToolIdentify


identified_object_data_t = namedtuple('identified_object_data_t', ['special_data', 'feature_id'],
                                      defaults=[None, None])


class IdentifyTool(QgsMapToolIdentify):
    """
    Инструмент для определения векторных слоев на канве.
    При создании экземпляра инструмента предоставляется возможность передать справочную информацию (reference_data).
    Инструмент может использоваться двумя способами:
    - стандартным для всех инструментов qgis (с помощью вызова метода start);
    - упрощенным (с помощью метода identify_by_event_position).
    При использовании стандартного способа испускается сигнал с идентифицированными данными.
    """
    data_identified = pyqtSignal(object, object)  # отправка данных о выбранных слоях (список, reference_data)

    def __init__(self, painter: MapCanvasPainter, reference_data=None, *, identify_invisible=False,
                 identify_one=False, identify_only_movable=False):
        super(IdentifyTool, self).__init__(painter.canvas)
        self.painter = painter
        self.identify_invisible = identify_invisible
        self.identify_one = identify_one
        self.identify_only_movable = identify_only_movable
        self.reference_data = reference_data
        self.resend_with_painter = True

    def start(self):
        self.drop()
        self.resend_with_painter = True
        self.painter.canvas.setMapTool(self)

    def finish(self):
        self.painter.canvas.use_default_tool()

    def drop(self):
        self.painter.canvas.use_default_tool()

    def identify_by_event_position(self, event_x: int, event_y: int) -> [identified_object_data_t]:
        """
        Аргументами являются координаты события, получаемые от канвы
        """
        # формирование списка слоев, среди которых идет идентификация
        layers_list = []
        for layer_id, is_visible in self.painter._objects_visibility_dict.items():
            layer = self.painter._objects_dict[layer_id]
            # проверка признака определяемости
            if not layer.special_data.is_definable:
                continue
            # проверка: если не разрешена идентификация скрытых слоев, то проверяем их видимость
            if not self.identify_invisible:
                if not is_visible:
                    continue
            # проверка признака перемещаемости объекта
            if (self.identify_only_movable and layer.special_data.is_movable) or (not self.identify_only_movable):
                layers_list.append(layer)
        # идентификация слоев
        identified = self.identify(event_x, event_y, layers_list)
        if len(identified) > 0:
            if self.identify_one:  # режим определения только одного слоя
                result = [self.object_data_from_identify_result(identified[0])]
            else:  # режим определения нескольких слоев
                result = [self.object_data_from_identify_result(identify_result) for identify_result in identified]
            # рассылка через рисовальщик
            if self.resend_with_painter:
                self.painter.broadcast_identified_data(result, self.reference_data)
            return result
        return []

    def canvasPressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.resend_with_painter = True
            self.data_identified.emit(self.identify_by_event_position(e.x(), e.y()), self.reference_data)
            self.resend_with_painter = False

    def canvasReleaseEvent(self, e):
        if e.button() == QtCore.Qt.RightButton:
            self.finish()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.drop()

    @staticmethod
    def object_data_from_identify_result(identify_result) -> identified_object_data_t:
        return identified_object_data_t(special_data=identify_result.mLayer.special_data,
                                        feature_id=identify_result.mFeature.id())













