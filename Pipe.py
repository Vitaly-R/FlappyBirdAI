import random as r
import pygame
import os


class Pipe:

    __DEF_PIPE_X = 305
    __DEF_EDGE_X = 300
    __GAP = 100
    __EDGE_H = 10
    __EDGE_W = 50
    __PIPE_W = 40
    __EDGE_COLOR = (100, 0, 0)
    __PIPE_COLOR = (120, 0, 0)
    __SPEED = 2

    def __init__(self, screen_height):
        """
        Initializes the parameters of the pipe pair for a screen with the given height.
        :param screen_height: int.
        """
        self.__passed = False
        self.__pipe_x = self.__DEF_PIPE_X
        self.__edge_x = self.__DEF_EDGE_X
        self.__top_pipe_length = r.randint(self.__EDGE_H, screen_height - self.__EDGE_H - self.__GAP)
        self.__bot_edge_y = self.__top_pipe_length + self.__EDGE_H + self.__GAP
        self.__bot_pipe_y = self.__bot_edge_y + self.__EDGE_H
        self.__bot_pipe_length = screen_height - self.__bot_pipe_y
        self.__top_edge_pic = pygame.image.load(os.path.join('Images', 'Top_edge.png')).convert()
        self.__bot_edge_pic = pygame.image.load(os.path.join('Images', 'Bot_edge.png')).convert()
        self.__pipe_pic = pygame.image.load(os.path.join('Images', 'Pipe.png')).convert()

    def draw(self, screen):
        """
        Draws the pipe on the given screen object.
        :param screen: pygame screen.
        """
        for i in range(self.__top_pipe_length):
            screen.blit(self.__pipe_pic, (self.__pipe_x, i))
        screen.blit(self.__top_edge_pic, (self.__edge_x, self.__top_pipe_length))
        screen.blit(self.__bot_edge_pic, (self.__edge_x, self.__bot_edge_y))
        for i in range(self.__bot_pipe_length):
            screen.blit(self.__pipe_pic, (self.__pipe_x, i + self.__bot_pipe_y))

    def move(self):
        self.__pipe_x -= self.__SPEED
        self.__edge_x -= self.__SPEED

    def get_edge_right(self):
        return self.__edge_x + self.__EDGE_W

    def get_edge_left(self):
        return self.__edge_x - self.__EDGE_W

    def get_gap_top(self):
        return self.__top_pipe_length + self.__EDGE_H

    def get_gap_bot(self):
        return self.get_gap_top() + self.__GAP

    def in_top(self, x, y):
        """
        :param x: coordinate (int).
        :param y: coordinate (int).
        :return weather the given coordinate is in the top pipe.
        """
        return (self.__edge_x <= x <= (self.__edge_x + self.__PIPE_W)) and \
               (y <= (self.__top_pipe_length + self.__EDGE_H))

    def in_bot(self, x, y):
        """
        :param x: coordinate (int).
        :param y: coordinate (int).
        :return weather the given coordinate is in the bottom pipe.
        """
        return (self.__edge_x <= x <= (self.__edge_x + self.__PIPE_W)) and (self.__bot_edge_y <= y)

    def passed(self):
        return self.__passed

    def pass_pipe(self):
        self.__passed = True
