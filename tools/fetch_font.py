"""
Small helper script: downloads a sample TTF font into img/font.ttf
Usage:
    python tools/fetch_font.py
"""
import os
try:
    import requests
except Exception:
    requests = None

ROOT = os.path.dirname(os.path.dirname(__file__))
ASSET_DIR = os.path.join(ROOT, 'img')
FONT_PATH = os.path.join(ASSET_DIR, 'font.ttf')

FONT_URL = 'https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf'

if __name__ == '__main__':
    if os.path.exists(FONT_PATH):
        print('Font already exists at', FONT_PATH)
    else:
        if requests is None:
            print('requests package not available. Install with `pip install requests`')
            raise SystemExit(1)
        os.makedirs(ASSET_DIR, exist_ok=True)
        print('Downloading font...')
        r = requests.get(FONT_URL, stream=True)
        if r.status_code == 200:
            with open(FONT_PATH, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print('Downloaded font to', FONT_PATH)
        else:
            print('Failed to download font:', r.status_code)
