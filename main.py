# Author: Ido Barkan
# Hacker Simulator Game - Project
import sys

import pygame
from pygame import mixer

from utils import button
from utils.colors import *

WIDTH = 1920
HEIGHT = 1080
REFRESH_RATE = 60
BG = LIGHT_BLUE_4
DEFAULT_VOL = 0

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ARIAL_FONT = pygame.font.SysFont("arial", 25)


def game_over():
    pygame.quit()
    sys.exit()


class GameStates:
    def __init__(self):
        self.state = "intro"
        self.EXIT_BUTTON = button.Button(WIDTH - 30, 0, "X", BLACK, BG, ARIAL_FONT, False, RED, (30, 30), 5, 3, BLACK)

        self.volume = DEFAULT_VOL
        mixer.music.load("assets/music/bg.mp3")
        mixer.music.play(-1)
        mixer.music.set_volume(self.volume)
        self.mute = False
        self.volume_change_font = pygame.font.SysFont("arial", 100)
        self.back_button = button.Button(WIDTH / 2, HEIGHT - 50, "BACK", BLACK, BG, ARIAL_FONT, True, LIGHT_BLUE_3,
                                         (100, 50), 5, 3, BLACK)
        self.sound_button = button.ImageButton(WIDTH / 2, HEIGHT / 2 - 100, "assets/images/sound_on.png",
                                               "assets/images/sound_off.png", (100, 100), True)
        self.sound_up_button = button.Button(WIDTH / 2 + 150, HEIGHT / 2 - 100, "+", BLACK, BG, self.volume_change_font,
                                             True, GREEN, (100, 100))
        self.sound_down_button = button.Button(WIDTH / 2 - 150, HEIGHT / 2 - 100, "-", BLACK, BG,
                                               self.volume_change_font, True, RED, (100, 100))

        self.title_font = pygame.font.Font("assets/fonts/hackerchaos.otf", 200)
        self.title_text = self.title_font.render("Hacker Simulator", True, BLACK)
        self.main_font = pygame.font.Font("assets/fonts/main.otf", 60)
        self.training_button = button.Button(WIDTH / 2, HEIGHT / 2 - 100, "TRAINING", BLACK, BG, self.main_font, True,
                                             LIGHT_BLUE_3)
        self.versus_button = button.Button(WIDTH / 2, HEIGHT / 2 + 50, "1 VS 1", BLACK, BG, self.main_font, True,
                                           LIGHT_BLUE_3)
        self.settings_button = button.Button(WIDTH / 2, HEIGHT / 2 + 200, "SETTINGS", BLACK, BG, self.main_font, True,
                                             LIGHT_BLUE_3)

        # training
        self.desktop = pygame.image.load("assets/images/desktop.jpg")
        self.viscord_button = button.ImageButton(32, HEIGHT / 2 - 100, "assets/images/viscord.png","assets/images/viscord_hover.png", (50, 50), True)
        self.terminal_button = button.ImageButton(32, HEIGHT / 2, "assets/images/terminal.png", "assets/images/terminal_hover.png", (50, 50), True)
        self.browser_button = button.ImageButton(32, HEIGHT / 2 + 100, "assets/images/browser.png", "assets/images/browser_hover.png", (50, 50), True)
        self.money_font = pygame.font.SysFont("arial", 25)
        self.money_text = self.money_font.render("$0", True, BLACK)
        self.money = 0
        self.viscord = False
        self.terminal = False
        self.browser = False

    def state_manager(self):

        if self.state == "intro":
            self.intro()
        elif self.state == "training":
            self.training()
        elif self.state == "versus":
            self.versus()
        elif self.state == "settings":
            self.settings()
        elif self.state == "gameOver":
            game_over()
        elif self.state == "viscord":
            self.viscord()
        elif self.state == "terminal":
            self.terminal()
        elif self.state == "browser":
            self.browser()

    def intro(self):
        pygame.display.set_caption("Hacker Simulator")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "gameOver"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.EXIT_BUTTON.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "gameOver"
                if self.training_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "training"
                if self.versus_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "versus"
                if self.settings_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "settings"
        display.fill(BG)
        display.blit(self.title_text, (WIDTH / 2 - self.title_text.get_width() / 2, self.title_text.get_height() / 2))
        self.EXIT_BUTTON.draw(display, pygame.mouse.get_pos())
        self.training_button.draw(display, pygame.mouse.get_pos())
        self.versus_button.draw(display, pygame.mouse.get_pos())
        self.settings_button.draw(display, pygame.mouse.get_pos())
        pygame.display.update()

    def settings(self):
        pygame.display.set_caption("Settings")

        # Game Settings screen loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "gameOver"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.EXIT_BUTTON.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "gameOver"
                if self.back_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "intro"
                if self.sound_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.sound_button.toggle()
                    self.mute = not self.mute
                    if self.mute:
                        mixer.music.set_volume(0)
                    else:
                        mixer.music.set_volume(self.volume)
                if self.sound_up_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    if self.mute is False:
                        self.volume += 0.1
                        mixer.music.set_volume(self.volume)
                if self.sound_down_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    if self.mute is False:
                        self.volume -= 0.1
                        mixer.music.set_volume(self.volume)
        display.fill(BG)
        self.EXIT_BUTTON.draw(display, pygame.mouse.get_pos())
        self.back_button.draw(display, pygame.mouse.get_pos())
        self.sound_button.draw(display, pygame.mouse.get_pos())
        self.sound_up_button.draw(display, pygame.mouse.get_pos())
        self.sound_down_button.draw(display, pygame.mouse.get_pos())
        pygame.display.update()

    def training(self):
        pygame.display.set_caption("TRAINING")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "gameOver"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.EXIT_BUTTON.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "gameOver"
                if self.viscord_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.viscord = not self.viscord
                if self.terminal_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "terminal"
                if self.browser_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "browser"

        display.fill(BG)
        display.blit(self.desktop, (0, 0))
        menu = pygame.rect.Rect(-3, HEIGHT/2 - 150, 75, 300)
        pygame.draw.rect(display, BLACK, menu, 3)
        upper_menu = pygame.rect.Rect(0, -3, 1920, 33)
        pygame.draw.rect(display, BLACK, upper_menu, 3)
        fill_rect = pygame.rect.Rect(0, 0, 1920, 30)
        pygame.draw.rect(display, BG, fill_rect)
        self.EXIT_BUTTON.draw(display, pygame.mouse.get_pos())
        self.viscord_button.draw(display, pygame.mouse.get_pos())
        self.terminal_button.draw(display, pygame.mouse.get_pos())
        self.browser_button.draw(display, pygame.mouse.get_pos())
        self.money_text = self.money_font.render("$" + str(self.money), True, BLACK)
        display.blit(self.money_text, (10, 0))

        if self.viscord:
            viscord_app = pygame.rect.Rect(WIDTH / 2 + 150, HEIGHT / 2 - 500, 800, 700)
            pygame.draw.rect(display, GREY20, viscord_app, )
            viscord_title = pygame.rect.Rect(WIDTH / 2 + 150, HEIGHT / 2 - 500, 800, 50)
            pygame.draw.rect(display, BLACK, viscord_title, 3)
            viscord_font = pygame.font.Font("assets/fonts/main.otf", 20)
            viscord_title_text = viscord_font.render("viscord", True, LIGHT_GREY)
            display.blit(viscord_title_text, (WIDTH / 2 + 150 + (800 / 2 - viscord_title_text.get_width() / 2), HEIGHT / 2 - 500 + (50 / 2 - viscord_title_text.get_height() / 2)))
            viscord_sided_menu = pygame.rect.Rect(WIDTH / 2 + 150, HEIGHT / 2 - 500 + 47, 250, 653)
            pygame.draw.rect(display, BLACK, viscord_sided_menu, 3)
            # help contact will be at the top bottom viscord sided menu
            viscord_help_contact = button.Button(viscord_sided_menu.bottomleft[0]+3,viscord_sided_menu.bottomleft[1]-50, "HELP", BLACK, WHITE, viscord_font,False, GREEN,(244,47))
            viscord_help_contact.draw(display, pygame.mouse.get_pos())


        pygame.display.update()



# main_loop
def main():
    game = GameStates()
    # Main game loop
    running = True
    while running:
        game.state_manager()
        clock.tick(REFRESH_RATE)


if __name__ == '__main__':
    main()
