#!/usr/bin/env python3

import os
import sys
from pathlib import Path

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings


class WebAppWindow(QMainWindow):
    def __init__(self, url: str, title: str):
        super().__init__()
        
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 1200, 800)
        
        # Set up isolated storage per app
        app_dir = Path(__file__).resolve().parent
        data_dir = app_dir / "data"
        cache_dir = app_dir / "cache"
        data_dir.mkdir(parents=True, exist_ok=True)
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create persistent profile with isolated storage
        profile = QWebEngineProfile("appnera", self)
        profile.setPersistentStoragePath(str(data_dir))
        profile.setCachePath(str(cache_dir))
        
        # Set user agent to identify as Chrome on Linux
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        profile.setHttpUserAgent(user_agent)
        
        # Create web view with the profile
        self.browser = QWebEngineView()
        self.browser.setPage(self.browser.page().__class__(profile, self.browser))
        
        # Enable all necessary web features
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.FocusOnNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.AllowGeolocationOnInsecureOrigins, False)
        settings.setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, False)
        settings.setAttribute(QWebEngineSettings.JavascriptCanPaste, True)
        settings.setAttribute(QWebEngineSettings.DnsPrefetchEnabled, True)
        
        # Handle permission requests (notifications, media, etc.)
        self.browser.page().featurePermissionRequested.connect(self._handle_permission_request)
        
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)
    
    def _handle_permission_request(self, origin, feature):
        """Auto-grant necessary permissions for web app functionality"""
        from PyQt5.QtWebEngineWidgets import QWebEnginePage
        
        # Grant permissions for notifications, media, geolocation, etc.
        allowed_features = [
            QWebEnginePage.Notifications,
            QWebEnginePage.MediaAudioCapture,
            QWebEnginePage.MediaVideoCapture,
            QWebEnginePage.MediaAudioVideoCapture,
            QWebEnginePage.Geolocation,
            QWebEnginePage.DesktopVideoCapture,
            QWebEnginePage.DesktopAudioVideoCapture,
        ]
        
        if feature in allowed_features:
            self.browser.page().setFeaturePermission(
                origin, feature, QWebEnginePage.PermissionGrantedByUser
            )


def main():
    url = os.environ.get("APPNERA_URL", "https://example.com")
    title = os.environ.get("APPNERA_APP_NAME", "WebApp")
    
    # Enable hardware acceleration (if available)
    try:
        from PyQt5.QtCore import Qt
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except (ImportError, AttributeError):
        pass
    
    app = QApplication(sys.argv)
    window = WebAppWindow(url=url, title=title)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()