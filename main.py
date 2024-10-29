import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
from level0Background import Background

pygame.init()
pygame.display.set_caption("Mother")

WIDTH, HEIGHT = 900, 600
FPS = 60
PLAYER_VEL = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Custom coordinates for idle and run sprites
idleSprites = [
    (30, 48, 48, 80),
    (158, 48, 48, 80),
    (286, 48, 48, 80),
    (414, 48, 48, 80),
    (542, 48, 48, 80),
]

runSprites = [
    (23, 48, 64, 80),
    (152, 48, 64, 80),
    (280, 48, 64, 80),
    (409, 48, 64, 80),
    (537, 48, 64, 80),
    (665, 48, 64, 80),
    (792, 48, 64, 80),
    (920, 48, 64, 80),
]

# Flip function for sprite mirroring
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

# Loading sprites based on custom coordinates
def load_sprites(sprite_sheet_path, coords, flip_sprites=False):
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    sprites = []
    for x, y, width, height in coords:
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(x, y, width, height)
        surface.blit(sprite_sheet, (0, 0), rect)
        scaled_surface = pygame.transform.scale(surface, (width // 1.5, height // 1.5))  # Scale down by 1.5
        sprites.append(scaled_surface)
    if flip_sprites:
        return sprites, flip(sprites)
    return sprites

def get_block(size):
    path = join("assets", "terrain","underworld.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size), pygame.SRCALPHA , 32)
    rect = pygame.Rect(16 , 0 ,size,size)
    surface.blit(image , (0,0), rect)
    return pygame.transform.scale2x(surface)

# Player class
class Player(pygame.sprite.Sprite):
    
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.mask = None

        # Load the specific sprites based on coordinates
        self.idle_right, self.idle_left = load_sprites("assets/characters/hero/idle.png", idleSprites, True)
        self.run_right, self.run_left = load_sprites("assets/characters/hero/run.png", runSprites, True)
        self.sprites = self.idle_left  # Default to idle left

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        if self.x_vel != 0:
            self.sprites = self.run_left if self.direction == "left" else self.run_right
        else:
            self.sprites = self.idle_left if self.direction == "left" else self.idle_right

        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(self.sprites)
        self.sprite = self.sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x , self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win , offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

    handle_vertical_collision(player,objects, player.y_vel)

def draw(window , objects, offset_x):
    for obj in objects:
        obj.draw(window, offset_x)


def main(screen):
    clock = pygame.time.Clock()
    block_size = 96
    floor = [Block(i * block_size, HEIGHT - block_size + 50, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    background = Background()
    player = Player(100, 100, 24, 24)
    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player, floor)        
        background.draw(screen, offset_x)
        player.draw(screen, offset_x)
        draw(screen ,floor, offset_x)

        if((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel >0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel


        # Update the display
        pygame.display.flip()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(screen)
