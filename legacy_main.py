# Legacy copy of the earlier starter file (renamed from "import pygame")
# Kept for reference, not used directly by main build.

import pygame
import pickle
from os import path
import os

pygame.mixer.pre_init(44100, -16, 2, 512)
try:
    pygame.mixer.init()
except Exception:
    pass
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# define game variables
# (omitting the rest of the legacy file for brevity)
