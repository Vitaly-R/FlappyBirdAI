import pygame
import os


class FlappyBirdGUI:

    __SCREEN_W = 250
    __SCREEN_H = 600
    __BG_COLOR = (77, 255, 255)
    __TEXT_COLOR = (0, 0, 0)

    def __init__(self):
        self.__init_pygame()

    def __init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.__font = pygame.font.SysFont('David MS', 30, True)
        self.__screen = pygame.display.set_mode((self.__SCREEN_W, self.__SCREEN_H))
        self.__bg = pygame.image.load(os.path.join('Images', 'BG.png')).convert()

    def show_start_screen(self):
        messages, positions = self.__get_start_game_messages()
        self.__show_messages(messages, positions)
        return self.__wait_for_player_start()

    def __get_start_game_messages(self):
        text = self.__font.render('Press \'Enter\' to start', False, self.__TEXT_COLOR)
        position = (self.__SCREEN_W // 2 - text.get_width() // 2, self.__SCREEN_H // 5)
        return [text], [position]

    def draw_game_screen(self, pipes):
        self.__draw_bg()
        self.__draw_pipes(pipes)

    def __draw_bg(self):
        self.__screen.blit(self.__bg, (0, 0))

    def __draw_pipes(self, pipes):
        for pipe in pipes:
            pipe.draw(self.__screen)

    def show_win_game_screen(self):
        messages, positions = self.__get_win_game_messages()
        self.__show_messages(messages, positions)
        return self.__wait_for_player_restart()

    def __get_win_game_messages(self):
        congratulations_msg = self.__font.render('Congratulations!', False, self.__TEXT_COLOR)
        congratulations_pos = (self.__SCREEN_W // 2 - congratulations_msg.get_width() // 2, self.__SCREEN_H // 5)
        max_score_msg1 = self.__font.render('You have reached', False, self.__TEXT_COLOR)
        max_score_pos1 = (self.__SCREEN_W // 2 - max_score_msg1.get_width() // 2,
                          congratulations_pos[1] + congratulations_msg.get_height())
        max_score_msg2 = self.__font.render('max score!', False, self.__TEXT_COLOR)
        max_score_pos2 = (self.__SCREEN_W // 2 - max_score_msg2.get_width() // 2,
                          max_score_pos1[1] + congratulations_msg.get_height())
        restart_msg = self.__font.render('Press \'r\' to restart', False, self.__TEXT_COLOR)
        restart_pos = (self.__SCREEN_W // 2 - restart_msg.get_width() // 2,
                       max_score_pos2[1] + 2 * max_score_msg1.get_height())
        return [congratulations_msg, max_score_msg1, max_score_msg2, restart_msg], \
               [congratulations_pos, max_score_pos1, max_score_pos2, restart_pos]

    def show_game_over_screen(self):
        messages, positions = self.__get_game_over_messages()
        self.__show_messages(messages, positions)
        return self.__wait_for_player_restart()

    def __get_game_over_messages(self):
        game_over_msg = self.__font.render('Game Over!', False, self.__TEXT_COLOR)
        game_over_pos = (self.__SCREEN_W // 2 - game_over_msg.get_width() // 2, self.__SCREEN_H // 5)
        restart_msg = self.__font.render('Press \'r\' to restart', False, self.__TEXT_COLOR)
        restart_pos = (self.__SCREEN_W // 2 - restart_msg.get_width() // 2,
                       self.__SCREEN_H // 5 + game_over_msg.get_height())
        return [game_over_msg, restart_msg], [game_over_pos, restart_pos]

    def __show_messages(self, messages, positions):
        self.__screen.blit(self.__bg, (0, 0))
        for i in range(len(messages)):
            self.__screen.blit(messages[i], positions[i])
        pygame.display.flip()

    def get_screen(self):
        return self.__screen

    def get_font(self):
        return self.__font

    @staticmethod
    def __wait_for_player_restart():
        do = True
        start = False
        while do:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    do = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                    start = True
                    do = False
        return start

    @staticmethod
    def __wait_for_player_start():
        do = True
        start = False
        while do:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    do = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    start = True
                    do = False
        return start

    @staticmethod
    def get_width():
        return FlappyBirdGUI.__SCREEN_W

    @staticmethod
    def get_height():
        return FlappyBirdGUI.__SCREEN_H

    @staticmethod
    def end_game():
        pygame.font.quit()
        pygame.quit()
