"""Turn subfloor.html (an artifact-style fragment) into a self-contained page for the desktop app.

The Google Fonts links are replaced with the bundled fonts as data URIs, so the app never goes online.
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "subfloor.html"
FONTS = ROOT / "app" / "fonts"
OUT = ROOT / "app" / "web" / "index.html"

# (family, file, weight range)
FACES = [
    ("Bricolage Grotesque", "BricolageGrotesque.woff2", "200 800"),
    ("IBM Plex Sans", "IBMPlexSans.woff2", "100 700"),
    ("IBM Plex Mono", "IBMPlexMono-400.woff2", "400"),
    ("IBM Plex Mono", "IBMPlexMono-500.woff2", "500"),
]


def font_css():
    rules = []
    for family, file, weight in FACES:
        data = base64.b64encode((FONTS / file).read_bytes()).decode("ascii")
        rules.append(
            f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}"
        )
    return "\n".join(rules)


page = SRC.read_text(encoding="utf-8")
page, removed = re.subn(r'<link [^>]*fonts\.(googleapis|gstatic)\.com[^>]*>\n?', "", page)
if removed != 3:
    raise SystemExit(f"expected 3 Google Fonts <link> tags in {SRC.name}, found {removed}")
if "://" in page:
    raise SystemExit("subfloor.html still references an outside URL")

head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>:root{{color-scheme:light}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<style>
{font_css()}
</style>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(head + page + "\n</html>\n", encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB)")
