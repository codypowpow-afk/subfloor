"""Subfloor desktop app: opens the synth page in a native WebView2 window."""
import os
import socket
import sys

import webview

PREFERRED_PORT = 48231  # fixed port keeps the page origin stable, so saved settings survive restarts


def resource(*parts):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, *parts)


def free_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return port
        except OSError:
            return None


def main():
    storage = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Subfloor")
    os.makedirs(storage, exist_ok=True)

    webview.create_window(
        "Subfloor",
        resource("web", "index.html"),
        width=1140,
        height=940,
        min_size=(420, 600),
        background_color="#14161D",
    )
    webview.start(
        gui="edgechromium",
        http_server=True,
        http_port=free_port(PREFERRED_PORT),
        private_mode=False,
        storage_path=storage,
        icon=resource("icon.ico"),
    )


if __name__ == "__main__":
    main()
