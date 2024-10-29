import pygame
from config import *

class Background:
    def __init__(self):
        # Load and scale background images
        self.skyImage = pygame.image.load(SPRITESHEET_PATH_1 + "background.png").convert()
        self.skyImage = pygame.transform.scale(self.skyImage, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.midgroundImage = pygame.image.load(SPRITESHEET_PATH_1 + "middleground.png").convert_alpha()
        self.midgroundImage = pygame.transform.scale(self.midgroundImage, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Set parallax speeds for each layer
        self.sky_speed = 0.2
        self.midground_speed = 0.5

    def draw(self, screen, offset_x):
        # Calculate new x positions for each layer, correctly handling both positive and negative movement
        sky_x = int(-offset_x * self.sky_speed) % WINDOW_WIDTH
        midground_x = int(-offset_x * self.midground_speed) % WINDOW_WIDTH

        # Draw the sky image twice, ensuring it wraps seamlessly
        screen.blit(self.skyImage, (sky_x, 0))
        screen.blit(self.skyImage, (sky_x - WINDOW_WIDTH, 0) if sky_x > 0 else (sky_x + WINDOW_WIDTH, 0))

        # Draw the midground image twice, ensuring it wraps seamlessly
        screen.blit(self.midgroundImage, (midground_x, 0))
        screen.blit(self.midgroundImage, (midground_x - WINDOW_WIDTH, 0) if midground_x > 0 else (midground_x + WINDOW_WIDTH, 0))
