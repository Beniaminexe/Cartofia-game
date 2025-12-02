# Cartofia - Web build notes

This document explains how to prepare and build the project for the web (WASM, Emscripten) using `pygbag` (CLI `pgbag`).

Prerequisites
- Python 3.10+ (used 3.11 in dev)
- pip packages: `pygbag` (for web packaging), `pygame`
- pgbag requires emscripten build chain. See pgbag docs.

Install pgbag (via the `pygbag` package) for web builds (recommended):

```powershell
pip install -r requirements-web.txt
```

Build steps

```powershell
# Ensure you're in the project root
cd "c:\Users\stefa\OneDrive\Desktop\cartofia game"

# Convert pickled levels to JSON (optional)
python tools/convert_levels.py

# Build using pgbag (include img assets and level json files)
pgbag -t web -o dist/web main.py --add-file img/* --add-file level*.json

# Serve the dist/web directory using a static file server
# On Windows you can use 'python -m http.server' in that folder
cd dist/web
python -m http.server 8000
# Then open http://localhost:8000

Running quick smoke tests

```powershell
pip install -r requirements.txt
python -m pytest tests/test_smoke.py
```
```

Notes
- The game attempts to use `music.ogg` if available; otherwise it falls back to `music.mp3`.
- Fonts: If you want the same look across platforms (desktop & web), add a `font.ttf` into `img/` and the loader will use it.
 - Tools included:
	 - `tools/convert_levels.py` to convert pickled `level*_data` files into JSON `level*.json` files.
	 - `tools/convert_audio.py` to (optionally) convert MP3 files to OGG using ffmpeg or pydub.
	 - `tools/fetch_font.py` to download a sample font into `img/font.ttf` (requires `requests`).
 - Windows Build:
	 - `release/windows/build_win.bat` - simple PyInstaller build script to create a `release\windows\dist` directory with a runnable build.
	 - `release/windows/run_game.bat` - helper to run the built exe from the release folder.
- The code uses `utils.load_image` and `utils.load_sound` for robust loading and fallbacks.
- Level data:  converted into JSON to avoid pickling across platforms.

Troubleshooting
- If audio does not work in browser, try converting sounds to OGG; MP3 support may vary with the browser or build chain.
- If an asset fails to load, the loader prints a warning and shows a placeholder image but will not crash the game.
