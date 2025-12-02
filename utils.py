import os
import json
import pygame

ROOT_DIR = os.path.dirname(__file__)
ASSET_DIR = os.path.join(ROOT_DIR, 'img')
LEVELS_DIR = ROOT_DIR


def _full_path_in_assets(name):
    return os.path.join(ASSET_DIR, name)


def load_image(name, alpha=True, fallback_size=(64, 64)):
    path = _full_path_in_assets(name)
    try:
        img = pygame.image.load(path)
        return img.convert_alpha() if alpha else img.convert()
    except Exception as e:
        # fallback placeholder
        surf = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surf.fill((255, 0, 255, 255))
        print(f"[utils] Image load failed for {path}: {e}")
        return surf


def load_sound(name):
    path = _full_path_in_assets(name)
    try:
        snd = pygame.mixer.Sound(path)
        return snd
    except Exception as e:
        print(f"[utils] Sound load failed for {path}: {e}")
        # return a silent fallback Sound - use a short empty array if possible
        try:
            empty = pygame.mixer.Sound(buffer=bytes())
            return empty
        except Exception:
            return None


def default_font(size: int):
    # Try to load a bundled font; fallback to default sys font if not available
    bundled = os.path.join(ASSET_DIR, 'font.ttf')
    try:
        if os.path.exists(bundled):
            return pygame.font.Font(bundled, size)
    except Exception:
        pass
    return pygame.font.SysFont(None, size)


def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font, color, x: int, y: int, center=False):
    img = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
    else:
        rect = img.get_rect(topleft=(x, y))
    surface.blit(img, rect)
    return rect


def load_level_data(level_num):
    # Prefer json-based levels named level{n}.json
    json_path = os.path.join(LEVELS_DIR, f'level{level_num}.json')
    pickle_path = os.path.join(LEVELS_DIR, f'level{level_num}_data')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    if os.path.exists(pickle_path):
        try:
            import pickle
            with open(pickle_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"[utils] Failed to load pickled level {pickle_path}: {e}")
    print(f"[utils] No level data found for level{level_num}")
    return None
