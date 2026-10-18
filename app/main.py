"""Subfloor desktop app: shows the synth in its own native window, fully offline.

The page is loaded straight from memory (no local web server), and settings are
saved to %APPDATA%\\Subfloor\\settings.json through the js_api bridge.
"""
import os
import sys

import webview

DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Subfloor")
SETTINGS = os.path.join(DATA_DIR, "settings.json")


def resource(*parts):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)


class Api:
    def load(self):
        try:
            with open(SETTINGS, encoding="utf-8") as f:
                return f.read()
        except OSError:
            return None

    def save(self, text):
        os.makedirs(DATA_DIR, exist_ok=True)
        tmp = SETTINGS + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, SETTINGS)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(resource("web", "index.html"), encoding="utf-8") as f:
        html = f.read()

    webview.create_window(
        "Subfloor",
        html=html,
        js_api=Api(),
        width=1140,
        height=1000,
        min_size=(420, 600),
        background_color="#14161D",
    )
    webview.start(
        gui="edgechromium",
        private_mode=False,
        storage_path=os.path.join(DATA_DIR, "webview"),
        icon=resource("icon.ico"),
    )


if __name__ == "__main__":
    main()
