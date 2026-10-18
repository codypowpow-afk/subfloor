"""Draw the app icon: a sine wave over a sub-octave sine on a dark panel."""
import math
import pathlib

from PIL import Image, ImageDraw

OUT = pathlib.Path(__file__).resolve().parent.parent / "app" / "icon.ico"
S = 256

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((8, 8, S - 8, S - 8), radius=52, fill=(20, 22, 29, 255))


def wave(cycles, amp, color, width):
    pts = [(x, S / 2 - amp * math.sin(2 * math.pi * cycles * (x - 40) / (S - 80))) for x in range(40, S - 39)]
    d.line(pts, fill=color, width=width, joint="curve")


wave(0.5 * 2, 70, (62, 85, 115, 255), 14)
wave(2, 46, (140, 157, 255, 255), 16)
img.save(OUT, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print(f"wrote {OUT}")
