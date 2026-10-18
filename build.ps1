# Builds dist\Subfloor\ (the app folder) and dist\Subfloor-<version>-win-x64.zip.
# Run from the repo root: powershell -ExecutionPolicy Bypass -File build.ps1
# Needs: Python 3 (standard library only) and the .NET Framework 4.8 C# compiler that ships with Windows.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$version = "1.2.0"
$webview2 = "1.0.2903.40"
$csc = "$env:WINDIR\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
$out = "dist\Subfloor"

# 1. Self-contained page (fonts inlined, no outside URLs)
py -3 tools\build_page.py
if ($LASTEXITCODE) { throw "build_page.py failed" }

# 2. Microsoft's WebView2 SDK from nuget.org, cached in build\
$pkg = "build\webview2-$webview2"
if (-not (Test-Path $pkg)) {
    New-Item -ItemType Directory -Force build | Out-Null
    Invoke-WebRequest "https://www.nuget.org/api/v2/package/Microsoft.Web.WebView2/$webview2" -OutFile "build\webview2.zip" -UseBasicParsing
    Expand-Archive "build\webview2.zip" $pkg -Force
}
$lib = "$pkg\lib\net462"

# 3. Compile the launcher
if (Test-Path dist) { Remove-Item dist -Recurse -Force }
New-Item -ItemType Directory -Force $out | Out-Null
& $csc /nologo /target:winexe /platform:x64 /optimize+ `
    "/out:$out\Subfloor.exe" /win32icon:app\icon.ico /win32manifest:app\app.manifest `
    /r:System.dll /r:System.Drawing.dll /r:System.Windows.Forms.dll `
    "/r:$lib\Microsoft.Web.WebView2.Core.dll" "/r:$lib\Microsoft.Web.WebView2.WinForms.dll" `
    app\Subfloor.cs
if ($LASTEXITCODE) { throw "csc failed" }

# 4. Assemble the folder and zip it
Copy-Item "$lib\Microsoft.Web.WebView2.Core.dll", "$lib\Microsoft.Web.WebView2.WinForms.dll", "$pkg\runtimes\win-x64\native\WebView2Loader.dll" $out
New-Item -ItemType Directory -Force "$out\web", "$out\licenses" | Out-Null
Copy-Item app\web\index.html "$out\web"
Copy-Item "$pkg\LICENSE.txt" "$out\licenses\WebView2-LICENSE.txt"
Copy-Item app\fonts\OFL-*.txt "$out\licenses"
Copy-Item README.md "$out\README.md"

$zip = "dist\Subfloor-$version-win-x64.zip"
Compress-Archive -Path $out -DestinationPath $zip -Force
Write-Host "Built $out\Subfloor.exe and $zip"
