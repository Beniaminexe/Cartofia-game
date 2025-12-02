@echo off
REM Build a Windows release using PyInstaller and copy necessary assets.
REM Run this from the repository root (you can also double click the bat file).

REM Ensure the workspace and Python are set up:
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller























pause
necho Build finished. Release folder: release\windows\dist)    xcopy /E /I "img\*" release\windows\dist\img\ > nul    rem already included by add-data, but ensure fonts/assets copied toofor %%d in (img) do ()    copy /Y "%%f" release\windows\dist\ > nulfor %%f in (level*.json) do (
nREM Copy extra assets like level jsons just to be safexcopy /E /I dist\Cartofia\* release\windows\dist\ > nulif not exist release\windows\dist mkdir release\windows\dist
nREM Create release dir and copy build
n)    exit /b %ERRORLEVEL%    pause    echo PyInstaller failed with error %ERRORLEVEL%.if %ERRORLEVEL% NEQ 0 (pyinstaller --noconfirm --onedir --name Cartofia main.py --add-data "img;img"if exist build rd /s /q build
n
necho Building Cartofia with PyInstaller (one-dir)if exist dist rd /s /q distnREM Clean previous builds