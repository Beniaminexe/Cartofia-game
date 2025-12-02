@echo off
REM Build Cartofia for the web using pgbag
REM Usage: run from repository root in PowerShell or CMD

REM Ensure you have pgbag installed:
REM pip install pgbag

pgbag -t web -o dist/web main.py --add-file img/* --add-file level*.json --add-file tools/*

necho "Build finished. Serve dist/web with a static HTTP server (python -m http.server)." 