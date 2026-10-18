# Subfloor

A small mono sub-bass and bass synth for Windows.

- Four wave shapes (sine, triangle, square, saw), a sub oscillator one octave down, and a detuned second oscillator
- Drive, low-pass filter with resonance, ADSR envelope, glide
- Wobble LFO on the filter cutoff
- Arpeggiator: up, down, up/down, random, played order; 1/4 to 1/32 steps; 1–3 octaves; tempo and gate
- Live oscilloscope, five presets, on-screen and computer-keyboard playing

## Install

1. Download [`bin/Subfloor-1.2.0-win-x64.zip`](bin/Subfloor-1.2.0-win-x64.zip) (also on the [Releases](../../releases) page).
2. Right-click the zip → **Extract All**, and put the `Subfloor` folder wherever you like (for example `Documents` or `C:\Apps`).
3. Open the folder and double-click **Subfloor.exe**. To get it in the Start menu, right-click `Subfloor.exe` → **Pin to Start**.

Keep the files in the folder together: the exe needs the three DLLs and the `web` folder beside it.

The app opens in its own window and works fully offline: the fonts are built in and it makes no network connections. It draws its window with the WebView2 component that Windows 10 and 11 already include. Settings are saved in `%LOCALAPPDATA%\Subfloor`.

The exe isn't code-signed, so the first time you run it Windows SmartScreen may say it "protected your PC". Choose **More info → Run anyway**.

## Play it

| Key | Action |
| --- | --- |
| `A S D F G H J K L ;` | White notes |
| `W E T Y U O P` | Sharps |
| `Z` / `X` | Octave down / up |

Most laptop speakers can't reproduce anything below about 60 Hz, so use headphones or monitors for the sub range.

## Build it

You need Python 3 (standard library only). The C# compiler comes with Windows.

```powershell
powershell -ExecutionPolicy Bypass -File build.ps1
```

That builds the page, downloads Microsoft's WebView2 SDK from nuget.org into `build/` the first time, compiles `app/Subfloor.cs`, and writes `dist/Subfloor/` and `dist/Subfloor-1.2.0-win-x64.zip`.

## Layout

- `subfloor.html` is the whole synth (Web Audio, no libraries). Edit this file to change the sound or the UI.
- `app/Subfloor.cs` is the native window (WinForms + WebView2). It serves the page from the local `web` folder under a reserved `.example` host name, so nothing goes online, and it never opens a browser.
- `tools/build_page.py` turns the page into a self-contained HTML document, swapping the Google Fonts links for the fonts in `app/fonts`. `tools/make_icon.py` redraws the icon (needs Pillow).

## Licenses

`app/fonts` contains Bricolage Grotesque, IBM Plex Sans and IBM Plex Mono, all under the SIL Open Font License 1.1. The WebView2 DLLs are Microsoft's, redistributed under the license in `licenses/WebView2-LICENSE.txt` in the app folder.
