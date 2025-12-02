# Cartofia - Windows release

Steps to build and run a Windows version of the game using PyInstaller.

Prerequisites
- Windows machine with Python 3.10+ installed
- Git or a copy of the project folder

1) Prepare environment
```powershell
# From project root
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

2) Build the game
```powershell
# From project root
release\windows\build_win.bat
```
This will produce a directory `release\windows\dist\Cartofia` containing the Windows build (exe + bundled files).

3) Run the built game
```powershell
release\windows\run_game.bat
```

Notes
- The `build_win.bat` uses `pyinstaller --onedir` to avoid large single-file packing issues with dynamic assets (images, fonts, audio).
- The build includes `img/` and `level*.json`. Make sure fonts and music exist in `img/`.
- If you want a single-file portable build, you can change PyInstaller to `--onefile`, but you'll need to ensure asset access is handled properly (embedded or extracted).

Troubleshooting
- If `pyinstaller` is missing, install it manually with `pip install pyinstaller`.
- For proper audio playback on Windows, use OGG/WAV (convert MP3 to OGG if needed) and include in the `img/` folder.
- If the build fails, check the PyInstaller log in the `build` folder and the console output.
