#!/usr/bin/env python3

import os
from pathlib import Path

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")

from gi.repository import Gtk, WebKit2


def _get_app_dirs() -> tuple[Path, Path]:
    app_dir = Path(__file__).resolve().parent
    data_dir = app_dir / "data"
    cache_dir = app_dir / "cache"
    data_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    return data_dir, cache_dir


class WebAppWindow(Gtk.Window):
    def __init__(self, url: str, title: str):
        super().__init__(title=title)

        self.set_default_size(1200, 800)
        self.connect("destroy", Gtk.main_quit)

        data_dir, cache_dir = _get_app_dirs()
        manager = WebKit2.WebsiteDataManager(
            base_data_directory=str(data_dir),
            base_cache_directory=str(cache_dir),
        )
        context = WebKit2.WebContext.new_with_website_data_manager(manager)
        view = WebKit2.WebView.new_with_context(context)

        view.load_uri(url)
        self.add(view)


def main() -> None:
    url = os.environ.get("APPNERA_URL", "https://example.com")
    title = os.environ.get("APPNERA_APP_NAME", "WebApp")

    window = WebAppWindow(url=url, title=title)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()