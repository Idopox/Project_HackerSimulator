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
        self.viscord_button = button.ImageButton(32, HEIGHT / 2 - 100, "assets/images/viscord.png",
                                                 "assets/images/viscord_hover.png", (50, 50), True)
        self.terminal_button = button.ImageButton(32, HEIGHT / 2, "assets/images/terminal.png",
                                                  "assets/images/terminal_hover.png", (50, 50), True)
        self.browser_button = button.ImageButton(32, HEIGHT / 2 + 100, "assets/images/browser.png",
                                                 "assets/images/browser_hover.png", (50, 50), True)
        self.money_font = pygame.font.SysFont("arial", 25)
        self.money_text = self.money_font.render("$0", True, BLACK)
        self.money = 0
        self.viscord = False
        self.terminal = False
        self.browser = False
        self.curr_contact = "None"
        self.viscord_window = Viscord(WIDTH / 2 + 150, HEIGHT / 2 - 500, 800, 700, "viscord", GREY20, LIGHT_GREY)

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
                # if self.viscord:
                # if viscord_help_contact.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                # if self.curr_contact != "Help":
                #    self.curr_contact = "Help"
                # else:
                # self.curr_contact = "None"

        display.fill(BG)
        display.blit(self.desktop, (0, 0))
        menu = pygame.rect.Rect(-3, HEIGHT / 2 - 150, 75, 300)
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

            self.viscord_window.draw(display)
            self.viscord_window.move()

            if self.curr_contact == "Help":
                help_info_rect = pygame.rect.Rect(viscord_sided_menu.topright[0], viscord_sided_menu.topright[1],
                                                  250 - 6, 653 - 50)
                pygame.draw.rect(display, BLACK, help_info_rect)

        pygame.display.update()


# general application window parent class
class Application:
    def __init__(self, x, y, w, h, title, color, header_color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.title = title
        self.color = color
        self.header_color = header_color
        self.header_font = pygame.font.Font("assets/fonts/main.otf", 20)
        self.header_text = self.header_font.render(self.title, True, BLACK)
        self.header_rect = pygame.rect.Rect(self.x, self.y, self.w, 50)
        self.header_outline = pygame.rect.Rect(self.x, self.y, self.w, 50)
        self.application = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        self.application_outline = pygame.rect.Rect(self.x, self.y, self.w, self.h)
        self.rects = []
        self.rects.append(self.application)
        self.rects.append(self.application_outline)
        self.rects.append(self.header_rect)
        self.rects.append(self.header_outline)
        self.buttons = []

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.application)
        pygame.draw.rect(display, BLACK, self.application_outline, 3)
        pygame.draw.rect(display, self.header_color, self.header_rect)
        pygame.draw.rect(display, BLACK, self.header_outline, 3)
        display.blit(self.header_text, (self.x + (self.w / 2 - self.header_text.get_width() / 2),
                                        self.y + (self.header_rect.height / 2 - self.header_text.get_height() / 2)))

    # move the whole window with all the rects according to the mouse position while dragging the header rect with the mouse left click pressed down
    def move(self):
        if pygame.mouse.get_pressed()[0]:
            if self.header_rect.collidepoint(pygame.mouse.get_pos()):
                self.x = pygame.mouse.get_pos()[0] - self.header_rect.width / 2
                self.y = pygame.mouse.get_pos()[1] - self.header_rect.height / 2
                for rect in self.rects:
                    rect.x = self.x
                    rect.y = self.y
                for button in self.buttons:
                    button.x = self.x
                    button.y = self.y
                self.header_text = self.header_font.render(self.title, True, BLACK)
                self.header_rect.x = self.x
                self.header_rect.y = self.y


class Viscord(Application):
    def __init__(self, x, y, w, h, title, color, header_color):
        super().__init__(x, y, w, h, title, color, header_color)
        self.sided_menu = pygame.rect.Rect(self.x, self.y + self.header_rect.height, 250, self.h - self.header_rect.height)
        self.rects.append(self.sided_menu)
        self.contact_chat_rect = pygame.rect.Rect(self.sided_menu.topright[0], self.sided_menu.top,
                                                  self.application.right - self.sided_menu.right - 3,
                                                  self.application.bottom - self.header_rect.bottom - 3)
        self.help_contact = button.Button(self.sided_menu.bottomleft[0] + 3,
                                          self.sided_menu.bottomleft[1] - 50, "HELP", BLACK, WHITE,
                                          self.header_font, False, GREEN, (244, 47))
        self.rects.append(self.contact_chat_rect)
        self.buttons.append(self.help_contact)

    def draw(self, display):
        super().draw(display)
        pygame.draw.rect(display, BLACK, self.sided_menu, 3)
        pygame.draw.rect(display, LIGHT_SKY_BLUE_4, self.contact_chat_rect)
        self.help_contact.draw(display, pygame.mouse.get_pos())
        pygame.display.update()

    def move(self):
        super().move()
        self.sided_menu.x = self.x
        self.sided_menu.y = self.y + self.header_rect.height
        self.contact_chat_rect.x = self.sided_menu.topright[0]
        self.contact_chat_rect.y = self.sided_menu.top
        self.help_contact.x = self.sided_menu.bottomleft[0] + 3
        self.help_contact.y = self.sided_menu.bottomleft[1] - 50



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
