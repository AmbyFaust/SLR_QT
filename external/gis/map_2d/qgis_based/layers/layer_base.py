from qgis.core import (QgsVectorLayer, QgsField, QgsPalLayerSettings, QgsTextFormat, QgsVectorLayerSimpleLabeling,
                       QgsRasterLayer)

from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor

from abc import abstractmethod

from ....abstract import DrawableObject


class SpecialData:
    """
    Свойства отображаемого слоя
    """
    def __init__(self, *, identify_data=None, description: str = '', meta=None, is_definable=True, is_movable=False):
        self.identify_data = identify_data  # данные, по которым можно определить, что это за объект
        self.description = description if description is not None else ''  # текстовое описание объекта
        self.meta = meta  # любая вспомогательная информация
        self.is_definable = is_definable if self.identify_data is not None else False  # признак определяемости объекта
        self.is_movable = is_movable  # признак "перемещаемости" объекта


class VectorLayerBase(DrawableObject, QgsVectorLayer):
    """
    Базовый класс для отображаемых векторных слоев
    """
    def __init__(self, data: SpecialData, *args):
        super(VectorLayerBase, self).__init__(data)
        super(QgsVectorLayer, self).__init__(*args)

    def setup(self, geometry, style) -> bool:
        check = self._check(geometry, style)
        if not check or check is None:
            self.validity = False
            return False
        self._create_features(geometry, style)
        self.validity = True
        return True

    @abstractmethod
    def _check(self, geometry, style) -> bool:
        pass

    @abstractmethod
    def _create_features(self, geometry, style):
        pass

    def _set_feature_label(self, feature, label_tuple: (str, QColor, QColor)):
        self.dataProvider().addAttributes([QgsField('draw_label', QVariant.String)])
        self.updateFields()

        feature.setFields(self.fields())
        feature.setAttribute('draw_label', label_tuple[0])

        text_format = QgsTextFormat()
        text_format.setColor(label_tuple[1] if label_tuple[1] is not None else label_tuple[2])

        pal_settings = QgsPalLayerSettings()
        pal_settings.fieldName = 'draw_label'
        pal_settings.setFormat(text_format)
        pal_settings.placement = QgsPalLayerSettings.Placement.Line

        labeling = QgsVectorLayerSimpleLabeling(pal_settings)

        self.setLabeling(labeling)
        self.setLabelsEnabled(True)


class RasterLayerBase(DrawableObject, QgsRasterLayer):
    """
    Базовый класс для отображаемых растровых слоев (не то же самое, что и подложка)
    """
    def __init__(self, data: SpecialData, *args):
        super(RasterLayerBase, self).__init__(data)
        super(QgsRasterLayer, self).__init__(*args)

    def setup(self, style) -> bool:
        self._create_renderers()
        self.validity = self._setup(style)
        return self.validity

    @abstractmethod
    def _setup(self, style) -> bool:
        pass

    @abstractmethod
    def _create_renderers(self):
        pass




