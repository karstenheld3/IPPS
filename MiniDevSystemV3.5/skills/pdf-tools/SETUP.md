# PDF Tools Setup

Install tools locally in `[WORKSPACE_FOLDER]/../.tools/`.

## 1. Set Workspace Folder

```powershell
$workspaceFolder = (Get-Location).Path
$toolsDir = "$workspaceFolder\..\.tools"
$installerDir = "$toolsDir\_installer"
if (-not (Test-Path $toolsDir)) { New-Item -ItemType Directory -Path $toolsDir }
if (-not (Test-Path $installerDir)) { New-Item -ItemType Directory -Path $installerDir }
```

## 2. Verify Python

```powershell
python --version
```
Expected: Python 3.10+. If missing: https://python.org

## 3. Install 7-Zip

Required to extract Ghostscript NSIS installer. Full 7z.exe needed (not 7za.exe).

Check: `Test-Path "$toolsDir\7z\7z.exe"`

```powershell
$7zDir = "$toolsDir\7z"
Invoke-WebRequest -Uri "https://www.7-zip.org/a/7z2408-x64.msi" -OutFile "$installerDir\7z2408-x64.msi"
$tempDir = "$installerDir\7z-temp"
msiexec /a "$installerDir\7z2408-x64.msi" /qn TARGETDIR="$tempDir"
Start-Sleep -Seconds 3
Move-Item "$tempDir\Files\7-Zip" $7zDir -Force
Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
```

Verify: `& "$toolsDir\7z\7z.exe" --help | Select-Object -First 3`

## 4. Install Poppler

Provides `pdftoppm` for PDF-to-image conversion.

Check: `Test-Path "$toolsDir\poppler\Library\bin\pdftoppm.exe"`

```powershell
$popplerDir = "$toolsDir\poppler"
Invoke-WebRequest -Uri "https://github.com/oschwartz10612/poppler-windows/releases/download/v24.08.0-0/Release-24.08.0-0.zip" -OutFile "$installerDir\poppler.zip"
Expand-Archive -Path "$installerDir\poppler.zip" -DestinationPath $toolsDir -Force
$extractedFolder = Get-ChildItem $toolsDir -Directory | Where-Object { $_.Name -like "poppler-*" } | Select-Object -First 1
if ($extractedFolder) { Move-Item $extractedFolder.FullName $popplerDir -Force }
```

Verify: `& "$toolsDir\poppler\Library\bin\pdftoppm.exe" -v`

Create output folder:
```powershell
$jpgDir = "$toolsDir\_pdf_to_jpg_converted"
if (-not (Test-Path $jpgDir)) { New-Item -ItemType Directory -Path $jpgDir }
if (-not (Test-Path "$jpgDir\.gitkeep")) { New-Item -ItemType File -Path "$jpgDir\.gitkeep" }
```

## 5. Install QPDF

PDF transformations (merge, split, encrypt, decrypt, repair).

Check: `Test-Path "$toolsDir\qpdf\bin\qpdf.exe"`

```powershell
$qpdfDir = "$toolsDir\qpdf"
Invoke-WebRequest -Uri "https://github.com/qpdf/qpdf/releases/download/v12.3.0/qpdf-12.3.0-msvc64.zip" -OutFile "$installerDir\qpdf.zip"
Expand-Archive -Path "$installerDir\qpdf.zip" -DestinationPath $toolsDir -Force
$extractedFolder = Get-ChildItem $toolsDir -Directory | Where-Object { $_.Name -like "qpdf-*" } | Select-Object -First 1
if ($extractedFolder) { Move-Item $extractedFolder.FullName $qpdfDir -Force }
```

Verify: `& "$toolsDir\qpdf\bin\qpdf.exe" --version`

## 6. Install Ghostscript

PDF image compression/downsizing. Only NSIS installer available, extract with 7-Zip.

Check: `Test-Path "$toolsDir\gs\bin\gswin64c.exe"`

```powershell
$gsDir = "$toolsDir\gs"
Invoke-WebRequest -Uri "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10060/gs10060w64.exe" -OutFile "$installerDir\gs10060w64.exe"
& "$toolsDir\7z\7z.exe" x -y -o"$gsDir" "$installerDir\gs10060w64.exe"
Remove-Item "$gsDir\`$PLUGINSDIR" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$gsDir\*.nsis" -Force -ErrorAction SilentlyContinue
```

Verify: `& "$toolsDir\gs\bin\gswin64c.exe" --version`

## 7. Install uv/uvx

Python package runner for MCP servers.

Check: `uvx --version`

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Installs to `%USERPROFILE%\.local\bin\`. Restart terminal or refresh PATH:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
```

## 8. Install Python Dependencies

```powershell
pip install pdf2image Pillow
```

## 9. Cleanup (Optional)

```powershell
Remove-Item "$installerDir\*" -Force -ErrorAction SilentlyContinue
```

## Tool Locations

- **7-Zip**: `[WORKSPACE_FOLDER]/../.tools/7z/`
- **Poppler**: `[WORKSPACE_FOLDER]/../.tools/poppler/`
- **QPDF**: `[WORKSPACE_FOLDER]/../.tools/qpdf/`
- **Ghostscript**: `[WORKSPACE_FOLDER]/../.tools/gs/`
- **uv/uvx**: `%USERPROFILE%\.local\bin\`
- **Installers**: `[WORKSPACE_FOLDER]/../.tools/_installer/`
- **JPG output**: `[WORKSPACE_FOLDER]/../.tools/_pdf_to_jpg_converted/`