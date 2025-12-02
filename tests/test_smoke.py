import pygame
import utils
import main

pygame.init()

def test_load_level_and_assets():
    ld = utils.load_level_data(1)
    assert isinstance(ld, list), "Level data should be a list or similar"

    img = utils.load_image('sun.png')
    assert isinstance(img, pygame.Surface), "sun.png should load as Surface"

    snd = utils.load_sound('coin.wav')
    # snd may be None if audio not available; just ensure callable outcome
    # if loaded, it should be a Sound
    if snd:
        assert hasattr(snd, 'get_length'), "Loaded sound should have get_length"

    # Test World creation
    world = main.World(ld)
    assert hasattr(world, 'tile_list'), 'World should have tile_list'

if __name__ == '__main__':
    test_load_level_and_assets()
    print('Smoke tests passed')
