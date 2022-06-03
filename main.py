# Author: Ido Barkan
# Hacker Simulator Game - Project

import pygame
from utils.colors import *
from utils import button

WIDTH = 1920
HEIGHT = 1080
REFRESH_RATE = 60
BG = LIGHT_BLUE_4


def main():
    # Initialize Pygame
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hacker Simulator")
    clock = pygame.time.Clock()

    title_font = pygame.font.Font("assets/fonts/hackerchaos.otf", 200)
    title_text = title_font.render("Hacker Simulator", True, BLACK)
    main_font = pygame.font.Font("assets/fonts/main.ttf", 100)
    arial_font = pygame.font.SysFont("arial", 25)
    training_button = button.Button(WIDTH / 2, HEIGHT / 2 - 100, "TRAINING", BLACK, BG, main_font, True, LIGHT_BLUE_3)
    versus_button = button.Button(WIDTH / 2, HEIGHT / 2 + 50, "1 VS 1", BLACK, BG, main_font, True, LIGHT_BLUE_3)
    settings_button = button.Button(WIDTH / 2, HEIGHT / 2 + 200, "SETTINGS", BLACK, BG, main_font, True, LIGHT_BLUE_3)
    exit_button = button.Button(WIDTH - 30, 0, "X", BLACK, BG, arial_font, False, RED, 5, 3, BLACK, (30, 30))
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    running = False
        display.fill(BG)
        display.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, title_text.get_height() / 2))
        exit_button.draw(display, pygame.mouse.get_pos())
        training_button.draw(display, pygame.mouse.get_pos())
        versus_button.draw(display, pygame.mouse.get_pos())
        settings_button.draw(display, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(REFRESH_RATE)


if __name__ == '__main__':
    main()
