from FlappyBirdGame import FlappyBird
from HumanPlayer import HumanPlayer
from AIPlayer import AIPlayer
import pygame


class FlappyBirdPlayer:

    __MAX_SCORE = 150
    __MIN_PLAYERS = 1

    def __init__(self, as_ai=False, num_players=__MIN_PLAYERS):
        self.__as_ai = as_ai
        self.__n_players = num_players \
            if type(num_players) == int and as_ai and self.__MIN_PLAYERS < num_players else self.__MIN_PLAYERS
        self.__game = FlappyBird()
        self.__living_players = None
        self.__restart()
        self.__dead_players = list()
        self.__stop_games = False

    def set_players(self, players):
        if self.__as_ai:
            self.__living_players = players
            self.__n_players = len(players)
        else:
            self.__living_players = players[:1]
        self.__dead_players = list()

    def play(self):
        self.__game.start() if not self.__as_ai else None
        while self.__game.is_running():
            if not self.__game.is_over():
                self.__do_game_round()
            else:
                self.__game.close() if self.__as_ai else self.__end_current_game()
        self.__game.end()

    def __do_game_round(self):
        dead = self.__game.do_game_loop(self.__living_players)
        for player in dead:
            self.__living_players.remove(player)
            self.__dead_players.append(player)
        if 0 < len(self.__living_players):
            self.__update_player()
            self.__game.update()
            self.__check_win()
        else:
            self.__game.terminate()

    def __check_win(self):
        if self.__MAX_SCORE <= self.__living_players[0].get_score():
            self.__ai_win() if self.__as_ai else self.__human_win()

    def __human_win(self):
        if self.__game.win():
            self.__restart()
        else:
            self.__game.close()

    def __end_current_game(self):
        if self.__game.run_game_over():
            self.__restart()
        else:
            self.__game.close()

    def __restart(self):
        gui = self.__game.get_gui()
        width = gui.get_width()
        height = gui.get_height()
        self.__living_players = [HumanPlayer(width, height) for i in range(self.__n_players)] \
            if not self.__as_ai else [AIPlayer(width, height) for i in range(self.__n_players)]

    def __ai_win(self):
        self.__game.terminate()
        for player in self.__living_players:
            player.win()

    def __move(self):
        for player in self.__living_players:
            player.move()

    def __respond_as_human(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game.close()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for player in self.__living_players:
                    player.jump()

    def __respond_as_ai(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__stop_games = True
                self.__game.close()
        if self.__game.is_running():
            for player in self.__living_players:
                player.make_move(self.__game)

    def __draw(self):
        for player in self.__living_players:
            player.draw(self.__game.get_gui().get_screen(), self.__game.get_gui().get_font(),
                        player is self.__living_players[-1])
        if self.__as_ai:
            text = self.__game.get_gui().get_font().render('Survivors: ' + str(len(self.__living_players)),
                                                           False, (0, 0, 0))
            pos = (0, 17)
            self.__game.get_gui().get_screen().blit(text, pos)

    def __update_player(self):
        self.__respond_as_ai() if self.__as_ai else self.__respond_as_human()
        self.__move()
        self.__draw()

    def get_width(self):
        return self.__game.get_gui().get_width()

    def get_height(self):
        return self.__game.get_gui().get_height()

    def get_max_score(self):
        return self.__MAX_SCORE

    def get_living_players(self):
        return self.__living_players

    def get_dead_players(self):
        return self.__dead_players

    def should_stop(self):
        return self.__stop_games
