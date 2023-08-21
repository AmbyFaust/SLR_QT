from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtWebKitWidgets import QWebView, QWebPage


class WebEnginePage(QWebPage):
    js_console_message = pyqtSignal(str)  # сигнал испускается при получении сообщения от JS

    def __init__(self, parent=None):
        super(QWebPage, self).__init__(parent)

    # слот выполняется при получении сообщения от JS
    def javaScriptConsoleMessage(self, msg, line, source):
        self.js_console_message.emit(msg)


class WebViewMap(QWebView):
    map_reloaded = pyqtSignal()

    def __init__(self, url: QUrl = None):
        super(WebViewMap, self).__init__()
        self.web_engine_page = WebEnginePage()
        self.web_engine_page.networkAccessManager().sslErrors.connect(lambda reply: reply.ignoreSslErrors())

        self.setPage(self.web_engine_page)

        self.url = None
        if url is not None:
            self.update_url(url)

    def reload(self):
        self.load(self.url)
        self.map_reloaded.emit()

    def update_url(self, url: QUrl):
        self.url = url
        self.load(url)


