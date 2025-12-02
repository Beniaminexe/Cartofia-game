@echo off
REM Build a Windows release using PyInstaller and copy necessary assets.
REM Run this from the repository root.

echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM Clean previous builds
if exist build rd /s /q build
if exist dist rd /s /q dist

echo Building Cartofia with PyInstaller (one-dir)
pyinstaller --noconfirm --onedir --name Cartofia main.py --add-data "img;img"

if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller failed with error %ERRORLEVEL%.
    exit /b %ERRORLEVEL%
)

REM Ensure release directory exists
if not exist release\windows\dist mkdir release\windows\dist

REM Copy the built artifact (one-dir) to the release folder
xcopy /E /I "dist\Cartofia\*" release\windows\dist\ > nul

REM Copy level json and other assets (just to be safe)
xcopy /Y level*.json release\windows\dist\  > nul
xcopy /E /I img\ release\windows\dist\img\ > nul

echo Build finished. Release folder: release\windows\dist
exit /b 0