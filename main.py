import os
import pygame
import utils
from pygame import mixer
import pickle
from os import path
import asyncio
import sys
print(sys.executable)
print(sys.version)

# --- Safe audio init ---
IS_WEB = sys.platform == 'emscripten'
if IS_WEB:
    # Web builds should not try to use pulseaudio
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
else:
    os.environ.setdefault("SDL_AUDIODRIVER", "pulseaudio")
try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
except pygame.error as e:
    print(f"[Warning] Audio init failed: {e}")
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    try:
        pygame.mixer.init()
    except Exception:
        pass

pygame.init()

clock = pygame.time.Clock()
fps = 60

# # --- Fullscreen setup ---
# # display_info = pygame.display.Info()
# # screen_width = display_info.current_w
# # screen_height = display_info.current_h
# # screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
# # pygame.display.set_caption("Cartofia (Fullscreen)")

# if sys.platform == "emscripten":
#     screen = pygame.display.set_mode((1280, 720))  # fixed windowed size for browser
# else:
#     # Desktop version keeps fullscreen if you want
#     screen = pygame.display.set_mode((1280, 720))
#     # or: screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)



# # Off-screen surface for the fixed game world (1000×1000)
# GW, GH = 1000, 1000
# game_surface = pygame.Surface((GW, GH))

# # Scale factors: screen pixels → game pixels
# scale_x = screen_width / GW
# scale_y = screen_height / GH

# def screen_to_game_pos(pos):
#     return (pos[0] / scale_x, pos[1] / scale_y)

# --- 1000x1000 fixed game surface setup ---

# --- Screen setup (desktop + web friendly) ---

GW = 1000
GH = 1000  # logical game resolution

# IS_WEB = sys.platform == "emscripten"  # duplicated - the platform detection is set near audio init

# Fixed window everywhere; on desktop you can still toggle fullscreen with F11
# For web, use a larger display window and draw to a logical game surface (GW x GH) then scale
if IS_WEB:
    # On web, render to a logical game surface and scale to a larger canvas
    screen_width = 1280
    screen_height = 720
else:
    screen_width = GW
    screen_height = GH

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cartofia (Web)" if IS_WEB else "Cartofia")

# Logical off-screen surface for consistent rendering across devices (used for web scaling)
game_surface = pygame.Surface((GW, GH))

# Scale factors: screen pixels → game pixels
scale_x = screen_width / GW
scale_y = screen_height / GH

def screen_to_game_pos(pos):
    # Convert physical screen coords to game logical coords (useful for mouse handling on web)
    return (int(pos[0] / scale_x), int(pos[1] / scale_y))

# Global draw surface: either the logical `game_surface` for web or direct `screen` for desktop
DRAW_SURFACE = screen




# --- Fonts & colours ---
# Use bundled or default font helper
font = utils.default_font(70)
font_score = utils.default_font(30)

white = (255, 255, 255)
blue = (0, 0, 255)

# --- Game variables ---
tile_size = 50
game_over = 0
main_menu = True
level = 1
max_levels = 11
score = 0

# --- Load images ---
sun_img = utils.load_image('sun.png', alpha=True)
bg_img = utils.load_image('sky.png', alpha=False)
restart_img = utils.load_image('restart_btn.png', alpha=True)
start_img = utils.load_image('start_btn.png', alpha=True)
exit_img = utils.load_image('exit_btn.png', alpha=True)

# --- Load sounds ---
# Prefer OGG for web, fallback to MP3
music_path_ogg = os.path.join(utils.ASSET_DIR, 'music.ogg')
music_path_mp3 = os.path.join(utils.ASSET_DIR, 'music.mp3')
try:
    if os.path.exists(music_path_ogg):
        pygame.mixer.music.load(music_path_ogg)
    elif os.path.exists(music_path_mp3):
        pygame.mixer.music.load(music_path_mp3)
    pygame.mixer.music.play(-1, 0.0, 5000)
except Exception as e:
    print('[Warning] Music load failed:', e)

coin_fx = utils.load_sound('coin.wav')
if coin_fx:
    coin_fx.set_volume(0.5)
jump_fx = utils.load_sound('jump.wav')
if jump_fx:
    jump_fx.set_volume(0.5)
game_over_fx = utils.load_sound('game_over.wav')
if game_over_fx:
    game_over_fx.set_volume(0.5)


# Helper text drawing: use utils.draw_text(surface, text, font, color, x, y, center=False)


def reset_level(level):
    player.reset(100, GH - 130)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    world_data = utils.load_level_data(level)
    if not world_data:
        # Fallback to an empty 20x20 level
        world_data = [[0 for _ in range(20)] for __ in range(20)]
    world = World(world_data)
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world

# --- Button Class ---
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        # Use scaled mouse coords on web builds so the buttons map to logical game coordinates
        pos = screen_to_game_pos(pygame.mouse.get_pos()) if IS_WEB else pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        DRAW_SURFACE.blit(self.image, self.rect)
        # screen.blit(self.image, self.rect)  # original
        return action



# --- Player Class ---
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_a] and not key[pygame.K_d]:
                self.counter = 0
                self.index = 0
                self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]

            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            utils.draw_text(DRAW_SURFACE, "GAME OVER!", font, blue, GW // 2, GH // 2, center=True)
            if self.rect.y > 200:
                self.rect.y -= 5

        DRAW_SURFACE.blit(self.image, self.rect)
        # screen.blit(self.image, self.rect)  # original
        return game_over


    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        for num in range(1, 5):
            img_right = utils.load_image(f"c{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = utils.load_image("ghost.png")
        self.image = self.images_right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

# --- Environment Classes ---
class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_img = utils.load_image("dirt.png")
        grass_img = utils.load_image("grass.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    self.tile_list.append((img, img_rect))
                if tile == 3:
                    blob_group.add(Enemy(col_count * tile_size, row_count * tile_size + 15))
                if tile == 4:
                    platform_group.add(Platform(col_count * tile_size, row_count * tile_size, 1, 0))
                if tile == 5:
                    platform_group.add(Platform(col_count * tile_size, row_count * tile_size, 0, 1))
                if tile == 6:
                    lava_group.add(Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2)))
                if tile == 7:
                    coin_group.add(Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2)))
                if tile == 8:
                    exit_group.add(Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2)))
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            DRAW_SURFACE.blit(tile[0], tile[1])
            # screen.blit(tile[0], tile[1])  # original


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = utils.load_image("blob.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        super().__init__()
        img = utils.load_image("platform.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = utils.load_image("lava.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = utils.load_image("coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect(center=(x, y))

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        img = utils.load_image("exit.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect(topleft=(x, y))

# --- Setup ---
player = Player(100, GH - 130)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

world_data = utils.load_level_data(level)
if not world_data:
    world_data = [[0 for _ in range(20)] for __ in range(20)]
world = World(world_data)

restart_button = Button(GW // 2 - 50, GH // 2 + 100, restart_img)
start_button = Button(GW // 2 - 350, GH // 2, start_img)
exit_button = Button(GW // 2 + 150, GH // 2, exit_img)

# --- Main loop ---
async def main():
    
    global level
    global score
    global world
    global game_over
    global main_menu
    global DRAW_SURFACE
    run = True
    while run:
        clock.tick(fps)
        # Set the drawing surface depending on the target platform
        if IS_WEB:
            DRAW_SURFACE = game_surface
        else:
            DRAW_SURFACE = screen
        DRAW_SURFACE.blit(bg_img, (0, 0))
        # screen.blit(bg_img, (0, 0))  # original
        DRAW_SURFACE.blit(sun_img, (290, 150))
        # screen.blit(sun_img, (290, 150))  # original

        if main_menu:
            if exit_button.draw():
                run = False
            if start_button.draw():
                main_menu = False
        else:
            world.draw()
            if game_over == 0:
                blob_group.update()
                platform_group.update()
                if pygame.sprite.spritecollide(player, coin_group, True):
                    score += 1
                    coin_fx.play()
                utils.draw_text(DRAW_SURFACE, "X " + str(score), font_score, white, tile_size - 10, 10)
            blob_group.draw(DRAW_SURFACE)
            platform_group.draw(DRAW_SURFACE)
            lava_group.draw(DRAW_SURFACE)
            coin_group.draw(DRAW_SURFACE)
            exit_group.draw(DRAW_SURFACE)
            game_over = player.update(game_over)

            if game_over == -1:
                if restart_button.draw():
                    world = reset_level(level)
                    game_over = 0
                    score = 0
            if game_over == 1:
                level += 1
                if level <= max_levels:
                    world = reset_level(level)
                    game_over = 0
                else:
                    utils.draw_text(DRAW_SURFACE, "YOU WIN!", font, blue, GW // 2, GH // 2, center=True)
                    if restart_button.draw():
                        level = 1
                        world = reset_level(level)
                        game_over = 0
                        score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

        if IS_WEB:
            # Scale the logical game surface into the visible display for web builds
            scaled_surface = pygame.transform.smoothscale(game_surface, (screen_width, screen_height))
            screen.blit(scaled_surface, (0, 0))
            # screen.blit(scaled_surface, (0, 0))  # legacy approach
        pygame.display.flip()

    pygame.quit()
    await asyncio.sleep(0)  # yield to browser

if __name__ == "__main__":
    asyncio.run(main())
