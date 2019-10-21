import pygame
import numpy as np
from Player import Player


class AIPlayer (Player):
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self._img = pygame.image.load(r'AIBird.png')
        self.__w = np.random.normal(0, 1, 5)
        self.__fitness = 0

    def make_move(self, game):
        pipes = game.get_pipes()
        closest_pipe = pipes[0]
        min_dist = (closest_pipe.get_edge_left() - self.get_right_x()) + \
                   (closest_pipe.get_edge_right() - self.get_right_x())
        min_dist = min_dist if 0 < (closest_pipe.get_edge_right() - self.get_right_x()) else np.inf
        for pipe in pipes:
            dist = (pipe.get_edge_left() - self.get_right_x()) + \
                   (pipe.get_edge_right() - self.get_right_x())
            dist = dist if 0 < (pipe.get_edge_right() - self.get_right_x()) else np.inf
            if dist < min_dist:
                closest_pipe = pipe
                min_dist = dist
        params = np.array([self._y, closest_pipe.get_edge_left(), closest_pipe.get_edge_right(),
                           closest_pipe.get_gap_top(), closest_pipe.get_gap_bot()])
        super().jump() if self.__decide(params) else None

    def __decide(self, params):
        return 0.5 <= ((1 + np.exp(-(np.dot(self.__w, params))))**(-1))

    def set_weights(self, weights):
        self.__w = weights

    def reproduce(self, num_offsprings, mutation_rate):
        offsprings = [AIPlayer(self._width, self._height) for i in range(num_offsprings)]
        for offspring in offsprings:
            offspring.set_weights(self.__mutate(mutation_rate))
        return offsprings

    def __mutate(self, mutation_rate):
        return self.__w + np.random.normal(0, mutation_rate, 5)

    def get_weights(self):
        return self.__w

    @staticmethod
    def load_from_weights(path, width, height):
        file = open(path, 'r')
        as_strings = file.readline().strip('[\n]').split()
        file.close()
        weights = list()
        for s in as_strings:
            weights.append(float(s))
        player = AIPlayer(width, height)
        player.set_weights(weights)
        return player
