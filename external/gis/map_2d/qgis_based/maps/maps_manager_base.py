from abc import abstractmethod

from PyQt5.QtCore import QObject, pyqtSignal

from typing import List

from .layers_config import LayerInfo, LayerKind

from ..common.provider_type import ProviderType
from ..common.dataset_type import DatasetType
from ..common.layer_constructor import LayerData, make_raster, make_vector


class MapsManagerBase(QObject):
    maps_list_updated = pyqtSignal(object)

    @abstractmethod
    def update_layers(self, layers: List[LayerInfo]):
        pass

    @abstractmethod
    def visible_layers(self) -> list:
        pass

    @staticmethod
    def make_layer(layer_info: LayerInfo):
        layer_data = LayerData(
            layer_info.id, layer_info.name, layer_info.url,
            ProviderType.provider_type_by_str(layer_info.provider),
            DatasetType.local if layer_info.is_local else DatasetType.network
        )
        return make_raster(layer_data) if layer_info.kind is LayerKind.Raster else make_vector(layer_data)


