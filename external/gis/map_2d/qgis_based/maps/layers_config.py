import json
import os
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional


class LayerKind(IntEnum):
    Raster = 0
    Vector = 1

    @staticmethod
    def kind_by_num(num):
        if num == 0:
            return LayerKind.Raster
        return LayerKind.Vector


@dataclass
class LayerInfo:
    id: str
    name: str
    url: str
    kind: LayerKind = LayerKind.Raster
    provider: str = 'wms'
    is_local: bool = False
    visible: bool = True


class LayersConfigData:
    def __init__(self, project_config_path: str, config_path: Optional[str] = None,
                 config_visibility_path: Optional[str] = None):
        self.data: List[LayerInfo] = []
        self.config_path = None
        self.config_visibility_path = None
        self.set_configs_pathes(project_config_path, config_path, config_visibility_path)
        self.__check_config_files()
        self.load()

    def set_configs_pathes(self, project_config_path: str, layers_config, visibility_config):
        if layers_config is None or not os.path.exists(layers_config):
            self.config_path = os.path.join(project_config_path, 'template_maps.json')
        else:
            self.config_path = layers_config

        if visibility_config is None or not os.path.exists(visibility_config):
            self.config_visibility_path = os.path.join(project_config_path, 'template_maps_visibility.json')
        else:
            self.config_visibility_path = visibility_config

    def load(self):
        self.data.clear()
        try:
            with open(self.config_path, "rt", encoding='utf-8') as layers_config_file, \
                    open(self.config_visibility_path, "rt", encoding='utf-8') as config_visibility_file:
                json_object = json.load(layers_config_file)
                visibility_json_object = json.load(config_visibility_file)
                self.data = [LayerInfo(id=li["id"], name=li["name"], url=li["url"], kind=LayerKind(li["kind"]),
                                       provider=li["provider"], is_local=li["is_local"],
                                       visible=visibility_json_object.get(li["id"], False))
                             for li in json_object]
        except BaseException as exp:
            print(f'Не удалось обработать конфигурационные файлы ([{self.config_path}] и '
                  f'[{self.config_visibility_path}])карт.\n{exp}')
            self.data = []

    def save(self):
        try:
            with open(self.config_path, "wt", encoding='utf-8') as layers_config_file, \
                    open(self.config_visibility_path, "wt", encoding='utf-8') as config_visibility_file:
                json_object = [{
                    "id": li.id,
                    "name": li.name,
                    "url": li.url,
                    "kind": li.kind.value,
                    "provider": li.provider,
                    "is_local": li.is_local,
                } for li in self.data]
                visibility_json_object = {li.id: li.visible for li in self.data}
                json.dump(json_object, layers_config_file, ensure_ascii=False, indent=2)
                json.dump(visibility_json_object, config_visibility_file, ensure_ascii=False, indent=2)
        except BaseException as exp:
            print(f'Не удалось сохранить конфигурационные файлы карт.\n{exp}')
            json.dump([], layers_config_file, ensure_ascii=False, indent=2)
            json.dump({}, config_visibility_file, ensure_ascii=False, indent=2)

    def __check_config_files(self):
        if not os.path.exists(self.config_visibility_path):
            try:
                with open(self.config_visibility_path, "wt", encoding='utf-8') as config_visibility_file:
                    json.dump({}, config_visibility_file, ensure_ascii=False, indent=2)
            except BaseException as exp:
                print(exp)


if __name__ == '__main__':
    from pprint import pprint

    layers_data = LayersConfigData()
    pprint(layers_data.data)
    layers_data.save()
