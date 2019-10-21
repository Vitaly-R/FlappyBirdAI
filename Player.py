import pygame
import random


class Player:

    _A = 1.5
    _MIN_INIT_V = -15
    _TERMINAL_V = 15
    _L = 20

    def __init__(self, screen_width, screen_height):
        self._score = 0
        self._width = screen_width
        self._height = screen_height
        self._x = screen_width // 5
        self._y = screen_height // 2
        self._v = random.randint(self._MIN_INIT_V, 0)
        self._img = pygame.image.load(r'DefBird.png')
        self._won = False

    def move(self):
        self._y = max(self._y + self._v, self._L // 2)
        self._v = min(self._v + self._A, self._TERMINAL_V)

    def add_score(self):
        self._score += 1

    def jump(self):
        self._v = int(0.7 * self._MIN_INIT_V)

    def draw(self, screen, font, show_score=True):
        screen.blit(self._img, (self._x - self._L // 2, self._y - self._L // 2))
        text = font.render('Score: ' + str(self._score), False, (0, 0, 0))
        screen.blit(text, (0, 0)) if show_score else None

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_left_x(self):
        return self._x - self._L // 2

    def get_right_x(self):
        return self._x + self._L // 2

    def check_collision(self, pipe):
        in_top = (pipe.in_top(self._x - self._L // 2, self._y - self._L // 2)) or \
                 (pipe.in_top(self._x - self._L // 2, self._y + self._L // 2)) or \
                 (pipe.in_top(self._x + self._L // 2, self._y - self._L // 2)) or \
                 (pipe.in_top(self._x + self._L // 2, self._y + self._L // 2))

        in_bot = (pipe.in_bot(self._x - self._L // 2, self._y - self._L // 2)) or \
                 (pipe.in_bot(self._x - self._L // 2, self._y + self._L // 2)) or \
                 (pipe.in_bot(self._x + self._L // 2, self._y - self._L // 2)) or \
                 (pipe.in_bot(self._x + self._L // 2, self._y + self._L // 2))

        return in_top or in_bot

    def get_score(self):
        return self._score

    def make_move(self, game):
        pass

    def get_weights(self):
        return 0

    def win(self):
        self._won = True

    def won(self):
        return self._won
