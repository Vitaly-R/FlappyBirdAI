from FlappyBirdPlayer import FlappyBirdPlayer
from AIPlayer import AIPlayer
from datetime import datetime
import os


class Trainer:
    def __init__(self, gen_size=10, max_gens=10, mutation_rate=0.1):
        self.__gen_size = gen_size
        self.__max_gens = max_gens
        self.__mutation_rate = mutation_rate
        self.__player = FlappyBirdPlayer(True, self.__gen_size)
        self.__players = [AIPlayer(self.__player.get_width(), self.__player.get_height())
                          for _ in range(self.__gen_size)]
        self.__best = None
        if not os.path.exists(os.path.join(os.getcwd(), 'weights')):
            os.mkdir(os.path.join(os.getcwd(), 'weights'))

    def train(self, save=True):
        for i in range(1, self.__max_gens + 1):
            print('Training generation', i, 'out of', self.__max_gens)
            self.__train_single_gen()
            if not self.__progress():
                break
        self.__save_best_weights() if self.__best is not None and save else None

    def __train_single_gen(self):
        self.__player = None
        self.__player = FlappyBirdPlayer(True, self.__gen_size)
        self.__player.set_players(self.__players)
        self.__player.play()

    def __progress(self):
        if not self.__player.should_stop():
            self.__find_best_player()
            self.__create_next_gen()
            return not self.__best.won()
        return False

    def __find_best_player(self):
        living_players = self.__player.get_living_players()
        if 0 < len(living_players):
            best = living_players[0]
        else:
            dead_players = self.__player.get_dead_players()
            best = dead_players[0]
            for player in dead_players[1:]:
                if best.get_score() < player.get_score():
                    best = player
        self.__best = best if self.__best is None or self.__best.get_score() < best.get_score() else self.__best

    def __create_next_gen(self):
        self.__players = self.__best.reproduce(self.__gen_size, self.__mutation_rate)

    def __save_best_weights(self):
        now = str(datetime.now().strftime("%d%m%Y %H%M%S"))
        weights = open(os.path.join(os.path.join(os.getcwd(), 'weights'), now + ' score ' + str(self.__best.get_score()) + '.txt'), 'w')
        weights.write(str(self.__best.get_weights()) + '\n')
        weights.close()
