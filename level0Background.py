import pygame
from config import *

class Background():
    def __init__(self):
        # Load and scale background images
        self.skyImage = pygame.image.load(SPRITESHEET_PATH_1 + "background.png").convert()
        self.skyImage = pygame.transform.scale(self.skyImage, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.midgroundImage = pygame.image.load(SPRITESHEET_PATH_1 + "middleground.png").convert_alpha()
        self.midgroundImage = pygame.transform.scale(self.midgroundImage, (WINDOW_WIDTH, WINDOW_HEIGHT))


    def update(self):
     pass

    def draw(self,screen):
        screen.blit(self.skyImage, (0,0))
        screen.blit(self.midgroundImage,(0,0))

