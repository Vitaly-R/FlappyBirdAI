import pygame
from FlappyBirdGUI import FlappyBirdGUI
from Pipe import Pipe


class FlappyBird:

    __RATE = 30

    def __init__(self):
        self.__gui = FlappyBirdGUI()
        self.__init_game_params()
        self.__run = True
        self.__end_game = False
        self.__rate = self.__RATE

    def __init_game_params(self):
        self.__pipes = [Pipe(self.__gui.get_height())]
        self.__clock = pygame.time.Clock()

    def start(self):
        self.__run = self.__gui.show_start_screen()

    def terminate(self):
        self.__end_game = True

    def close(self):
        self.__run = False

    def run_game_over(self):
        if self.__gui.show_game_over_screen():
            self.__end_game = False
            self.__init_game_params()
            return True
        return False

    def win(self):
        self.__run = self.__gui.show_win_game_screen()

    def end(self):
        self.__gui.end_game()

    def do_game_loop(self, players):
        self.__update_pipes(players)
        dead = self.__check_collisions(players)
        self.__gui.draw_game_screen(self.__pipes)
        return dead

    def update(self):
        pygame.display.flip()
        self.__clock.tick(self.__rate)

    def __update_pipes(self, players):
        remove = list()
        for pipe in self.__pipes:
            if pipe.get_edge_right() <= 0:
                remove.append(pipe)
            else:
                pipe.move()
                if pipe.get_edge_right() < players[0].get_left_x() and not pipe.passed():
                    pipe.pass_pipe()
                    for player in players:
                        player.add_score()
        for pipe in remove:
            self.__pipes.remove(pipe)
        if len(self.__pipes) == 0 or self.__pipes[-1].get_edge_right() <= players[0].get_x():
            self.__pipes.append(Pipe(self.__gui.get_height()))

    def __check_collisions(self, players):
        dead = list()
        for player in players:
            if self.__gui.get_height() <= player.get_y():
                dead.append(player)
            else:
                for pipe in self.__pipes:
                    if player.check_collision(pipe):
                        dead.append(player)
        self.__end_game = len(players) == 0
        return dead

    def add_pipe(self):
        self.__pipes.append(Pipe(self.__gui.get_height()))

    def is_running(self):
        return self.__run

    def is_over(self):
        return self.__end_game

    def get_pipes(self):
        return self.__pipes

    def get_gui(self):
        return self.__gui
