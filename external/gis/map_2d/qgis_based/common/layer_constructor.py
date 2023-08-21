import os

from qgis.core import QgsRasterLayer, QgsVectorLayer

from .dataset_type import DatasetType
from .provider_type import ProviderType


class LayerData:
    def __init__(self, id: str = '', name: str = '', url: str = '',
                 provider: ProviderType = ProviderType.none,
                 dataset: DatasetType = DatasetType.local):
        self.id = id
        self.name = name
        self.url = url
        self.provider = provider
        self.dataset = dataset

    def prepare_url(self):
        return self.url if self.dataset is not DatasetType.local else os.path.abspath(
            os.path.join(os.path.dirname(__file__), self.url)
        )


def make_raster(layer_data: LayerData) -> QgsRasterLayer:
    return QgsRasterLayer(layer_data.prepare_url(), layer_data.id, layer_data.provider.provider_str) \
        if layer_data.provider is not ProviderType.none else QgsRasterLayer(layer_data.prepare_url(), layer_data.id)


def make_vector(layer_data: LayerData) -> QgsVectorLayer:
    return QgsVectorLayer(layer_data.prepare_url(), layer_data.id, layer_data.provider.provider_str) \
        if layer_data.provider is not ProviderType.none else QgsVectorLayer(layer_data.prepare_url(), layer_data.id)






