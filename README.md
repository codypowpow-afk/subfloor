# Subfloor

A small mono sub-bass and bass synth for Windows.

- Four wave shapes (sine, triangle, square, saw), a sub oscillator one octave down, and a detuned second oscillator
- Drive, low-pass filter with resonance, ADSR envelope, glide
- Wobble LFO on the filter cutoff
- Arpeggiator: up, down, up/down, random, played order; 1/4 to 1/32 steps; 1–3 octaves; tempo and gate
- Live oscilloscope, five presets, on-screen and computer-keyboard playing

## Run it

Download `Subfloor.exe` from the [Releases](../../releases) page and double-click it. It opens in its own window and works fully offline: the fonts are built in, there is no local web server, and it makes no network connections. It draws its window with the WebView2 component that Windows 10 and 11 already include.

Windows SmartScreen may warn you the first time because the exe isn't code-signed. Choose **More info → Run anyway**.

## Play it

| Key | Action |
| --- | --- |
| `A S D F G H J K L ;` | White notes |
| `W E T Y U O P` | Sharps |
| `Z` / `X` | Octave down / up |

Most laptop speakers can't reproduce anything below about 60 Hz, so use headphones or monitors for the sub range.

## Build it

You need Python 3.10 or newer.

```powershell
powershell -ExecutionPolicy Bypass -File build.ps1
```

That creates `.venv`, installs the pinned packages, wraps `subfloor.html` into `app/web/index.html`, and writes `dist/Subfloor.exe`.

## Layout

- `subfloor.html` is the whole synth (Web Audio, no libraries). Edit this file to change the sound or the UI.
- `app/main.py` opens it in a native window using [pywebview](https://pywebview.flowrl.com/).
- `tools/build_page.py` turns the page into a self-contained HTML document, swapping the Google Fonts links for the fonts in `app/fonts`; `tools/make_icon.py` draws the icon.

Settings are saved to `%APPDATA%\Subfloor\settings.json`.

## Fonts

`app/fonts` contains Bricolage Grotesque, IBM Plex Sans and IBM Plex Mono, all under the SIL Open Font License 1.1 (license files alongside).
