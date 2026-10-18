"""Wrap subfloor.html (an artifact-style fragment) in a full HTML document for the desktop app."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "subfloor.html"
OUT = ROOT / "app" / "web" / "index.html"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(HEAD + SRC.read_text(encoding="utf-8") + "\n</html>\n", encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)}")
