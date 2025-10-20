@echo off
REM ======================================================
REM  Cartofia Auto-Detecting Build Script (Windows)
REM  Handles missing icon + Microsoft Store Python issues
REM  Author: Beniaminexe
REM ======================================================

setlocal enabledelayedexpansion
echo.
echo 🧩 Cleaning previous build...
rmdir /s /q build >nul 2>&1
rmdir /s /q dist >nul 2>&1
rmdir /s /q release >nul 2>&1
del cartofia.spec >nul 2>&1

echo.
echo 🚀 Detecting PyInstaller path...
REM Default possible locations (Store + normal installs)
set "PYINSTALLER="
if exist "%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe" (
    set "PYINSTALLER=%LOCALAPPDATA%\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts\pyinstaller.exe"
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\Scripts\pyinstaller.exe" (
    set "PYINSTALLER=%LOCALAPPDATA%\Programs\Python\Python311\Scripts\pyinstaller.exe"
)
if exist "%ProgramFiles%\Python311\Scripts\pyinstaller.exe" (
    set "PYINSTALLER=%ProgramFiles%\Python311\Scripts\pyinstaller.exe"
)

if "%PYINSTALLER%"=="" (
    echo ❌ Could not find PyInstaller! Installing locally...
    python -m pip install pyinstaller
    for /f "delims=" %%i in ('where pyinstaller 2^>nul') do set "PYINSTALLER=%%i"
)

if "%PYINSTALLER%"=="" (
    echo ❌ PyInstaller still not found. Exiting.
    pause
    exit /b 1
)

echo Found PyInstaller at: %PYINSTALLER%
echo.

REM ===== Optional icon handling =====
set "ICON_ARG="
if exist "cartofia.ico" (
    set "ICON_ARG=--icon cartofia.ico"
    echo 🎨 Using custom icon: cartofia.ico
) else (
    echo ⚠️  No icon found — skipping icon embedding.
)

echo.
echo 🧠 Building Cartofia executable...
"%PYINSTALLER%" --onefile --noconsole ^
--add-data "img;img" ^
--add-data "level1_data;." ^
%ICON_ARG% ^
cartofia.py

if %errorlevel% neq 0 (
    echo ❌ Build failed! Check the error log above.
    pause
    exit /b 1
)

echo.
echo 📦 Preparing release folder...
mkdir release
move dist\cartofia.exe release\ >nul
xcopy img release\img /E /I /Y >nul
if exist level1_data copy level1_data release\ >nul

echo.
echo ✅ Build complete!
echo Your game is ready in the "release" folder:
echo     release\cartofia.exe
echo.
pause
