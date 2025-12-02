@echo off
REM Run the built Cartofia release (one-dir build expected)
SETLOCAL ENABLEDELAYEDEXPANSION
cd /d "%~dp0\dist"
if exist Cartofia\Cartofia.exe (
    cd Cartofia
    Cartofia.exe
) else (
    REM maybe the exe is in dist directly
    if exist Cartofia.exe (
        Cartofia.exe
    ) else (
        echo Can't find Cartofia.exe — ensure the release build exists in this folder.
        pause
    )
)
