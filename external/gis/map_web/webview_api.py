from PyQt5.QtCore import QObject, QTimer, QCoreApplication
from PyQt5 import QtCore

from abc import abstractmethod
from typing import Tuple, Union

import copy

from .webview_map import WebViewMap


class WebViewApi(QObject):
    def __init__(self, web_map: WebViewMap):
        super(WebViewApi, self).__init__(None)
        self.web_map = web_map

        self._page = web_map.web_engine_page
        self._page.js_console_message.connect(self._parse_js_console_message, type=QtCore.Qt.DirectConnection)

        self._answer_buffer = None           # буфер для хранения ответов от JS
        self._answer_waiting_timeout = 2000  # мсек
        self._answer_error_buffer = ''       # буфер для хранения ошибок при ожидании ответа от JS

    def set_answer_waiting_timeout(self, msec: int):
        if not isinstance(msec, int):
            return
        if msec < 0:
            return
        self._answer_waiting_timeout = msec

    def post(self, action_type: str, message_json: dict):
        """
        Метод для отправки сообщения JavaScript без ожидания ответа
        """
        self._send_message(action_type, message_json)

    def get(self, action_type: str, message_json: dict) -> Tuple[Union[None, object], str]:
        """
        Метод для отправки сообщения JavaScript с ожиданием ответа
        """
        self._send_message(action_type, message_json)

        self._answer_buffer = None

        timer = QTimer()
        timer.setSingleShot(True)
        timer.start(self._answer_waiting_timeout)

        # либо буфер заполнится, либо будет достигнут timeout
        while self._answer_buffer is None:
            QCoreApplication.processEvents()
            if not timer.isActive():
                return None, 'Превышено время ожидания ответа от JS'
            if self._answer_error_buffer:
                err_buf = self._answer_error_buffer
                self._answer_error_buffer = ''
                return None, err_buf
            continue

        ret = copy.deepcopy(self._answer_buffer)  # копируем значение буфера
        self._answer_buffer = None                # сброс значения буфера

        return ret, ''

    def _send_message(self, action_type: str, message_json):
        self._page.currentFrame().evaluateJavaScript('window.frames.vseuz.postMessage({actionType: \'' +
                                                     str(action_type) +
                                                     '\', param: \'' +
                                                     str(message_json) +
                                                     '\'}, \'*\');')

    @abstractmethod
    def _parse_js_console_message(self, msg: str):
        """
        Метод для парсинга сообщений от JavaScript.
        При выполнении запросов с ожиданием ответа, в методе необходимо заполнять буфер с ответом от JavaScript.
        """
        pass


