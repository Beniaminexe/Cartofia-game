@echo off
REM Build Cartofia for the web using pygbag (pygbag package) to produce a web build
REM Usage: run from repository root in PowerShell or CMD

REM Ensure you have pgbag installed:
REM pip install pygbag

python -m pygbag --build --html --title Cartofia "%CD%\main.py"
if exist build\web (
	if exist dist\web rd /s /q dist\web
	xcopy /E /I "build\web\*" dist\web\ > nul
)

necho "Build finished. Serve dist/web with a static HTTP server (python -m http.server)." 