import copy

from typing import Optional, List

from .layers_config import LayersConfigData, LayerInfo

from .maps_manager_base import MapsManagerBase


class MapsManager(MapsManagerBase):
    def __init__(self, project_config_path: str,
                 config_path: Optional[str] = None,
                 config_visibility_path: Optional[str] = None):
        super(MapsManager, self).__init__(None)
        self.layers_config = LayersConfigData(project_config_path, config_path, config_visibility_path)
        self.layers = [None for _ in self.layers_config.data]

    def update_layers(self, layers: List[LayerInfo]):
        self.layers_config.data = copy.deepcopy(layers)
        self.layers_config.save()
        self.layers_config.load()
        self.layers = [None] * len(self.layers_config.data)
        self.maps_list_updated.emit(self.layers_config.data)

    def visible_layers(self):
        visible_layers = []
        for i in range(len(self.layers)):
            if self.layers_config.data[i].visible:
                if self.layers[i] is None:
                    self.layers[i] = self.make_layer(self.layers_config.data[i])
                visible_layers.append(self.layers[i])
        return visible_layers



