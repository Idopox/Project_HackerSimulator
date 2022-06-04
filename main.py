# Author: Ido Barkan
# Hacker Simulator Game - Project
import sys

import pygame
from utils.colors import *
from utils import button

WIDTH = 1920
HEIGHT = 1080
REFRESH_RATE = 60
BG = LIGHT_BLUE_4

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ARIAL_FONT = pygame.font.SysFont("arial", 25)

class GameStates:
    def __init__(self):


        self.state = "intro"
        self.back_button = button.Button(WIDTH / 2, HEIGHT - 50, "BACK", BLACK, BG, ARIAL_FONT, True, LIGHT_BLUE_3,
                                    (100, 50), 5, 3, BLACK)
        self.sound_button = button.ImageButton(WIDTH / 2, HEIGHT / 2 - 100, "assets/images/sound_on.png",
                                          "assets/images/sound_off.png", (100, 100), True)
        self.title_font = pygame.font.Font("assets/fonts/hackerchaos.otf", 200)
        self.title_text = self.title_font.render("Hacker Simulator", True, BLACK)
        self.main_font = pygame.font.Font("assets/fonts/main.otf", 60)
        self.training_button = button.Button(WIDTH / 2, HEIGHT / 2 - 100, "TRAINING", BLACK, BG, self.main_font, True,
                                        LIGHT_BLUE_3)
        self.versus_button = button.Button(WIDTH / 2, HEIGHT / 2 + 50, "1 VS 1", BLACK, BG, self.main_font, True, LIGHT_BLUE_3)
        self.settings_button = button.Button(WIDTH / 2, HEIGHT / 2 + 200, "SETTINGS", BLACK, BG, self.main_font, True,
                                        LIGHT_BLUE_3)
        self.EXIT_BUTTON = button.Button(WIDTH - 30, 0, "X", BLACK, BG, ARIAL_FONT, False, RED, (30, 30), 5, 3, BLACK)


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
            self.gameOver()

    def intro(self):
        pygame.display.set_caption("Hacker Simulator")



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.EXIT_BUTTON.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "gameOver"
                if self.training_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    training_screen()
                if self.versus_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    versus_screen()
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
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.EXIT_BUTTON.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "gameOver"
                if self.back_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "intro"
                if self.sound_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.sound_button.toggle()
        display.fill(BG)
        self.EXIT_BUTTON.draw(display, pygame.mouse.get_pos())
        self.back_button.draw(display, pygame.mouse.get_pos())
        self.sound_button.draw(display, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(REFRESH_RATE)

    def gameOver(self):
        pygame.quit()
        sys.exit()


# main_loop
def main():
    global game
    game = GameStates()
    # Main game loop
    running = True
    while running:
        game.state_manager()
        clock.tick(REFRESH_RATE)


# training_screen
def training_screen():
    pygame.display.set_caption("Training")


def versus_screen():
    pygame.display.set_caption("Versus")


if __name__ == '__main__':
    main()
