# Builds dist\Subfloor.exe. Run from the repo root: powershell -ExecutionPolicy Bypass -File build.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path .venv)) { py -3 -m venv .venv }
$py = ".\.venv\Scripts\python.exe"
& $py -m pip install --quiet --disable-pip-version-check -r requirements.txt

& $py tools\build_page.py
if (-not (Test-Path app\icon.ico)) { & $py tools\make_icon.py }

& $py -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name Subfloor `
    --icon app\icon.ico `
    --add-data "app\web;web" `
    --add-data "app\icon.ico;." `
    app\main.py

Write-Host "Built dist\Subfloor.exe"
