# AGENT LOG — Project onboarding for AI agents

Summary
-------
This file provides a concise, actionable log of code changes, configuration edits, tooling additions, testing actions, and recommended next steps. It’s written to make it easy for other AI agents (or maintainers) to continue working on the project without missing context.

Date: 2025-12-02
Primary contact: project repo

High-level goals
----------------
- Make `main.py` robust for both desktop and web targets.
- Centralize asset handling and text drawing with `utils.py`.
- Convert pickled level data to JSON for cross-platform compatibility.
- Create helper tools and automation for build/test tasks on web (pgbag) and Windows (pyinstaller).
- Archive legacy files and keep old code as commented references.

Files added
-----------
- `utils.py` — centralized helper functions (image/sound loading, fonts, draw_text, level loader). See `utils.load_image`, `utils.load_sound`, `utils.default_font`, `utils.draw_text`, `utils.load_level_data`.
- `tools/convert_levels.py` — convert `levelN_data` pickles to `levelN.json`.
- `tools/convert_audio.py` — convert MP3 to OGG with ffmpeg/pydub.
- `tools/fetch_font.py` — optionally download a TTF font into `img/`.
- `tools/*` also included in packaging scripts where helpful.
- `tests/test_smoke.py` — minimal smoke tests (loads a level, loads an image and sound, constructs World).
- `release/windows/build_win.bat`, `release/windows/run_game.bat`, `release/windows/README_WINDOWS.md` — Windows packaging & run instructions using PyInstaller.
- `README_WEB.md` — web build instructions and troubleshooting.
- `build_web.bat` — helper to run `pgbag` for web packaging.
- `CONFIGURATION_CHANGES.txt` — a detailed change summary of significant modifications.
- `AGENT_LOG.md` — this agent-focused log (the current file).

Key file updates (main changes)
-------------------------------
- `main.py`:
  - Replaced numerous raw image/sound loads with `utils.load_image()` + `utils.load_sound()` to centralize asset handling and enable fallbacks.
  - Added `game_surface` (GW x GH) and `screen_to_game_pos` mapping.
  - Introduced `DRAW_SURFACE` to flexibly target the offscreen logical surface (web builds) or display `screen` (desktop builds).
  - Updated `Button.draw()` to use `screen_to_game_pos()` for web mouse mapping.
  - Replaced multiple `draw_text()` definitions with `utils.draw_text(DRAW_SURFACE, ...)` for consistency.
  - Updated group draws (blob_group/platform_group etc.) to draw to `DRAW_SURFACE`.
  - For web builds, `game_surface` is scaled to `screen` via `transform.smoothscale` each frame; for desktop, drawing is done directly to `screen` (no scaling). The previous scaling path was intentionally kept commented in the code for audit and fallback.
  - Added `IS_WEB` detection and guarded `SDL_AUDIODRIVER` selection for web audio fallback.
  - Left original (legacy) `screen.blit(...)` calls commented in many places for traceability.

- `level_editor.py`
  - Updated to use `utils.load_image()` for assets.
  - Save & load now prefer `level{n}.json` (JSON first), with pickle fallback for compatibility.
  - Text rendering uses `utils.draw_text`.

- Legacy file handling
  - `old.py`, `oldcode.py`, and the file named `import pygame` were archived into `oldversions/` and replaced with small placeholder files in the root to avoid accidental import/troubles.

Why these decisions were made
---------------------------
- Using a single helper module (`utils.py`) reduces duplication, simplifies cross-target fallback behavior, and provides a single location for asset-path configuration.
- Logical game surface + scaling is standard for web builds (maintains consistent logical resolution across differing screen sizes and DPI); it also enables a consistent gameplay experience whether on desktop or browser.
- JSON level files are portable across platforms and less prone to Python-version compatibility issues compared to pickles.
- Archiving old files prevents accidental imports and keeps the repo tidy but preserves historical code for reference.

Testing performed & test scripts
-------------------------------
- `tests/test_smoke.py` was added and executed; it checks:
  - `utils.load_level_data(1)` loads a 20x20 list.
  - `utils.load_image('sun.png')` returns a pygame surface.
  - `utils.load_sound('coin.wav')` returns a pygame Sound or None (depending on environment).
  - `main.World()` constructs correctly using the loaded level data.

Run the tests locally:
```powershell
pip install -r requirements.txt
python -m pytest tests/test_smoke.py
```

How to run the game locally (desktop)
-------------------------------------
```powershell
pip install -r requirements.txt
python main.py
```

How to build/test for the Web (pgbag)
------------------------------------
```powershell
pip install pygbag
python tools/convert_levels.py  # convert pickled levels to JSON
python tools/fetch_font.py  # optional (downloads a TTF to img/)
python tools/convert_audio.py img/music.mp3 img/music.ogg  # optional
  python -m pygbag --build --html --title Cartofia "$PWD/main.py"
cd dist/web
python -m http.server 8000
# open http://localhost:8000 in a browser
```

How to build for Windows (PyInstaller)
-------------------------------------
- Build script placed in `release/windows/build_win.bat` (uses PyInstaller `--onedir`). Example flow:
```powershell
pip install -r requirements.txt
pip install pyinstaller
release\windows\build_win.bat
# The built folder should be in release\windows\dist (one-dir build)
release\windows\run_game.bat  # to run the exe
```

Notable caveats & open questions for other agents
-----------------------------------------------
- `IS_WEB` detection uses `sys.platform == 'emscripten'` during runtime; when testing web builds locally you may rely on specific pgbag flags that set `sys.platform` or other flags; test thoroughly in a browser (Chrome recommended).
- If you revert to `game_surface`-less approach (desktop-only), some code (like `screen_to_game_pos`) can be removed.
- `font.ttf` is not bundled by default — if you want cross-platform typography, add a TTF to `img/` and optionally run `tools/fetch_font.py`.
- Player input mapping on web relies on `screen_to_game_pos()`; make sure UI elements and buttons use this function for correct hit detection.
- I left the original (pre-change) `screen.blit` lines commented out; agents may choose to fully remove them once the new approach is validated.

Priority next steps for other agents
-----------------------------------
1. Convert all remaining legacy `pygame.image.load('img/..')` calls in other files (like `oldcode`, `import pygame` legacy copies) to `utils.load_image()` to centralize behavior.
2. Add `img/font.ttf` and optionally replace SysFont usage entirely with `pygame.font.Font('img/font.ttf', size)` for consistency across platforms.
3. Convert audio files to OGG (`tools/convert_audio.py`) and remove `mp3` fallback if OGG is working across browsers.
4. Add a GitHub Actions workflow that runs `pytest` and produces both a web bundle (`pgbag`) and a Windows artifact (`pyinstaller`), uploading artifacts to GitHub releases.
5. Consider refactoring the app into a `Game` class or `Application` to reduce global state.

Reverting changes (quick tips)
-----------------------------
- Use Git to revert files; previously created `oldversions/` contains legacy copies if needed. Because we used patch edits, revert specific files with `git restore <file>` if necessary.

Agent TODO (for AI agents onboarding) 
------------------------------------
- Verify web build with `pgbag` using `README_WEB.md` steps and report console errors / broken features.
- Validate colliders, input mapping, and sound behavior in the browser.
- Validate Windows build script produces a working EXE and that the game uses local assets correctly.
- Inspect the `utils.py` helpers for additional improvements (e.g., support .ogg/.wav push fallback, logging levels instead of silent print). 

Contact & notes
---------------
- I left code comments and placeholders for transparency. If you need me to refactor further (e.g., `Game` object, CI, asset packaging tweaks), state the desired next step and I will implement it.

---

End of AGENT_LOG
## Change History (auto-updated quick log)

- [2025-12-02 09:48:00Z] (done) Implemented `utils.py` for centralized asset handling: load_image, load_sound, default_font, draw_text, and load_level_data.
- [2025-12-02 09:50:00Z] (done) Replaced multiple `draw_text` occurrences with `utils.draw_text(surface, ...)` across `main.py` and `level_editor.py`.
- [2025-12-02 09:52:00Z] (done) Converted `levelN_data` pickle files to JSON using `tools/convert_levels.py` and created `level*.json` files.
- [2025-12-02 09:54:00Z] (done) Added `tools/convert_audio.py` (pydub/ffmpeg fallback) and `tools/fetch_font.py` to help package fonts and audio for web.
- [2025-12-02 09:57:00Z] (done) Replaced direct `pygame.image.load` and `pygame.mixer.Sound` calls with `utils.load_image` and `utils.load_sound`.
- [2025-12-02 09:59:00Z] (done) Created `tests/test_smoke.py` and executed smoke test; installed pytest and validated smoke test OK.
- [2025-12-02 10:05:00Z] (done) Implemented web support: introduced `game_surface` (GWxGH), `scale_x`, `scale_y`, `screen_to_game_pos`, and `DRAW_SURFACE` to render to logical surface and scale to the screen for web builds.
- [2025-12-02 10:08:00Z] (done) Updated `main.py` to draw all game content to `DRAW_SURFACE` and added web scaling to the main loop.
- [2025-12-02 10:09:00Z] (done) Updated input handling for web: `screen_to_game_pos` mapped and used for UI interactions.
- [2025-12-02 10:13:00Z] (done) Added `release/windows/` scripts: `build_win.bat`, `run_game.bat`, `README_WINDOWS.md` to support Windows PyInstaller builds.
- [2025-12-02 10:16:00Z] (done) Added `build_web.bat` and `README_WEB.md` updates to document pgbag packaging for web builds.
- [2025-12-02 10:20:00Z] (done) Archived legacy files (`old.py`, `import pygame`, `oldcode.py`) into `oldversions/`; left placeholders in root for traceability.
- [2025-12-02 10:22:00Z] (done) Created `AGENT_LOG.md` and `CONFIGURATION_CHANGES.txt` to document changes and config.
- [2025-12-02 10:27:00Z] (done) Added `game_wrapper.py` as a minimal wrapper that supports both async and sync entrypoints for `main.py`.
- [2025-12-02 10:30:00Z] (done) Added `.github/workflows/ci.yml` to run pytest, attempt web build with pgbag, and Windows build with PyInstaller.
- [2025-12-02 10:35:00Z] (done) Added `.vscode/tasks.json` to provide Run/Build tasks for desktop, web and Windows.
- [2025-12-02 10:38:00Z] (done) Added `tools/log_task.py` as a simple script other agents can run to append timestamped entries to `AGENT_LOG.md`.
- [2025-12-08 20:20:00Z] (done) Refreshed `main.py` web loop: added debug overlay for first frames, per-frame logging, and stronger web menu skip; ensured scaling uses logical surface each frame.
- [2025-12-08 20:32:00Z] (done) Rebuilt web bundle from scratch, recloned `build/web/archives`, and repacked `build/web/cartofia-game.apk` with assets/code under `assets/`; server now serves wheel + APK without 404.
- [2025-12-08 20:35:00Z] (pending) Snapshot: served current web build from `build/web` (archives cloned, `cartofia-game.apk` loads 200, wheel 200); browser still shows black canvas though console shows APK mount complete and audio blocked pending user click. Next: verify Python prints/overlay render on web and confirm `main.py` entry executes.
- [2025-12-08 20:45:00Z] (pending) Browser console log: pygbag bootstrap fetches wheel 200 and downloads `cartofia-game.apk` (size ~9.2MB) with BFS mount complete; canvas remains black, no visible debug overlay or Python stdout yet. Need to confirm if `main.py` executes (look for `[cartofia]` prints) and why scaled surface draws black despite mounted assets.
- [2025-12-08 20:55:00Z] (done) Fixed entry guard: `main.py` now calls `asyncio.run(main())` even on web, so pygbag will actually enter the async game loop (previously skipped due to IS_WEB guard, causing black canvas). Rebuild web bundle to pick up the change.
- [2025-12-08 21:05:00Z] (done) Hardened web rebuild script: `rebuild_web.sh` now creates `build/web` before running pygbag to avoid `FileNotFoundError` when writing `cartofia-game.html`; keeps cache clean with `rm -rf build/web build/web-cache` first.
- [2025-12-08 21:10:00Z] (done) Added `build/web-cache` creation in `rebuild_web.sh` so pygbag can cache `default.tmpl`/`favicon.png` and avoid CDN write errors when the cache dir is missing.
- [2025-12-08 21:20:00Z] (done) Manually repacked `build/web/cartofia-game.apk` (9.23MB) with `assets/` containing main.py, utils.py, web_main.py, game_wrapper.py, levels, img/, tests, etc., since pygbag did not emit the APK; archives recloned into `build/web/archives` for wheel serving.

## How to use the logging tool

1. Run the script:
   ```powershell
   python tools/log_task.py "Message about the task" [status]
   ```
   Example: `python tools/log_task.py "Added CI workflow" done`

2. The script updates `AGENT_LOG.md` with the timestamped entry under the "Change History" section.

3. Agents can call it during automated flows or CI runs to log build-and-test steps automatically.

## Live Task Updates

- Task: Implement GitHub Actions CI
  - [done] Status: added `.github/workflows/ci.yml` with test/build steps
- Task: Add VS Code tasks
  - [done] Status: added `.vscode/tasks.json`
- Task: Refactor main to use DRAW_SURFACE
  - [done] Status: added `game_surface`, `DRAW_SURFACE`, updated draws
- Task: Web scaling and input mapping
  - [done] Status: `screen_to_game_pos` and scaling implemented; UI adjusted to logical coords
- Task: Add build tools & helpers
  - [done] Status: added `tools/` scripts: convert_levels, convert_audio, fetch_font, log_task
