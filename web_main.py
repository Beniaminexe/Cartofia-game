import runpy
from pathlib import Path

# When this file runs (inside the browser), just run cartofia.py
runpy.run_path(
    str(Path(__file__).with_name("main.py")),
    run_name="__main__",
)
