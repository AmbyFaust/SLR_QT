from abc import abstractmethod

from ..abstract import Painter, DrawableObject
from .webview_api import WebViewApi


class WebDrawableObject(DrawableObject):
    pass


class WebMapPainter(Painter):

    def __init__(self, webview_api: WebViewApi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map_api = webview_api

    @abstractmethod
    def _set_object_visibility(self, object_id, visibility):
        pass

    @abstractmethod
    def _remove_object(self, object_id):
        pass

    @abstractmethod
    def _object_created(self, object_id, draw_hidden):
        pass

