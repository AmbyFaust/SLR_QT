from enum import Enum


class ProviderType(Enum):
    none = ''
    wms = 'wms'
    wmts = 'wmts'

    def __init__(self, provider_str: str):
        self.provider_str = provider_str

    @staticmethod
    def provider_type_by_str(type_str: str):
        if type_str == 'wms':
            return ProviderType.wms
        if type_str == 'wmts':
            return ProviderType.wmts
        return ProviderType.none
