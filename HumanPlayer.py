import pygame
from Player import Player


class HumanPlayer (Player):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self._img = pygame.image.load(r'HumanBird.png')
