#!/usr/bin/env python3

import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView


class WebAppWindow(QMainWindow):
    def __init__(self, url: str, title: str):
        super().__init__()
        
        # Set window size based on screen dimensions (85% of screen)
        screen = QApplication.primaryScreen().geometry()
        width = int(screen.width() * 0.85)
        height = int(screen.height() * 0.85)
        self.setGeometry(100, 100, width, height)
        self.setWindowTitle(title)

        # Set up the web engine view
        self.browser = QWebEngineView()
        
        # Set user agent to identify as Chrome on Linux (required for WhatsApp and other sites)
        profile = self.browser.page().profile()
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        profile.setHttpUserAgent(user_agent)
        
        self.browser.setUrl(QUrl(url))

        # Enable persistent storage (cookies, cache, etc.)
        self.browser.settings().setAttribute(self.browser.settings().LocalStorageEnabled, True)
        self.browser.settings().setAttribute(self.browser.settings().LocalContentCanAccessFileUrls, True)
        self.browser.settings().setAttribute(self.browser.settings().LocalContentCanAccessRemoteUrls, True)

        self.setCentralWidget(self.browser)


def main():
    url = os.environ.get("APPNERA_URL", "https://example.com")
    title = os.environ.get("APPNERA_APP_NAME", "WebApp")
    
    app = QApplication(sys.argv)
    window = WebAppWindow(url=url, title=title)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()