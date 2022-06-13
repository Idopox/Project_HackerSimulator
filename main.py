# Author: Ido Barkan
# Hacker Simulator Game - Project
import pickle
import random as rnd
import socket
import sys
import threading
import time

import pygame
from pygame import mixer

from utils import button
from utils import tcp_by_size as sr
from utils.colors import *

WIDTH = 1920
HEIGHT = 1080
REFRESH_RATE = 60
BG = LIGHT_BLUE_4
DEFAULT_VOL = 0
RANDOM_WORDS_LIST = ["ink", "historical", "caption", "medical", "garrulous", "snakes", "lake", "pour", "mountainous",
                     "cactus", "extra-small", "rake", "apple", "jar", "drop",
                     "tiger", "tired", "toy"]
SERVICES = ["http", "ssh", "ftp", "smb"]

display = None
ARIAL_FONT = None


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
        self.viscord_window = Viscord(WIDTH / 2 + 150, HEIGHT / 2 - 500, 800, 700, LIGHT_GREY, self)
        self.terminal_window = Terminal(WIDTH / 2 + 150, HEIGHT / 2 - 500, 800, 700, LIGHT_GREY, self)
        self.objectives = Objectives(self)
        self.completed_objectives = []
        self.online = False

    def init_training(self):
        self.objectives.add_objective("1")
        self.objectives.add_objective("1")
        self.objectives.add_objective("2")
        self.objectives.add_objective("3")
        self.objectives.add_objective("4")

    def init_online(self):
        self.join_button = button.Button(WIDTH / 2, HEIGHT / 2 - 100, "JOIN", BLACK, BG, self.main_font, True,
                                         LIGHT_BLUE_3)
        self.game_started = False
        self.enemy_objectives_completed = 0
        self.enemy_objectives_total = 0
        self.enemy_name = "None"
        self.won = None
        self.online = True
        self.game = Versus(self)
        self.terminal_window.versus = self.game
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
                    self.init_training()
                if self.versus_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    self.state = "versus"
                    self.init_online()
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
                if event.button == 1:
                    if self.EXIT_BUTTON.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        self.state = "gameOver"
                    if self.viscord_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        self.viscord = not self.viscord
                    if self.terminal_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        self.terminal = not self.terminal
                    if self.browser_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        self.browser = not self.browser
                    if self.terminal_window.IO_rect.collidepoint(
                            (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        self.terminal_window.active = True
                    else:
                        self.terminal_window.active = False
                    for contact in self.viscord_window.contacts:
                        if self.viscord_window.contacts[contact]["button"].isOver((pygame.mouse.get_pos()[0],
                                                                                   pygame.mouse.get_pos()[1])):
                            if self.viscord_window.active_contact == contact:
                                self.viscord_window.active_contact = None
                                self.viscord_window.display_default_chat(display)
                            else:
                                self.viscord_window.display_default_chat(display)
                                self.viscord_window.active_contact = self.viscord_window.contacts[contact]
                                self.viscord_window.display_contact_chat(contact, display)
                if event.button == 3:
                    if self.terminal_window.active:
                        text = pygame.scrap.get(pygame.SCRAP_TEXT).decode("utf-8")[:-1]
                        if text:
                            self.terminal_window.active_input(display, text)

            if event.type == pygame.KEYDOWN:
                if self.terminal_window.active:
                    self.terminal_window.active_input(display, event)

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

        if self.terminal:
            self.terminal_window.draw(display)
            self.terminal_window.move()
            if self.terminal_window.download_thread is not None and self.terminal_window.download_thread.is_alive() and not self.terminal_window.downloading:
                self.terminal_window.download_thread.join()

        pygame.display.update()

    def versus(self):
        pygame.display.set_caption("VERSUS")

        if not self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "gameOver"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.EXIT_BUTTON.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        self.state = "gameOver"
                    if self.join_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        self.game.connect(display)
                display.fill(BG)
                self.EXIT_BUTTON.draw(display, pygame.mouse.get_pos())
                self.join_button.draw(display, pygame.mouse.get_pos())

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "gameOver"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.EXIT_BUTTON.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                            self.state = "gameOver"
                        if self.viscord_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                            self.viscord = not self.viscord
                        if self.terminal_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                            self.terminal = not self.terminal
                        if self.browser_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                            self.browser = not self.browser
                        if self.terminal_window.IO_rect.collidepoint(
                                (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                            self.terminal_window.active = True
                        else:
                            self.terminal_window.active = False
                        for contact in self.viscord_window.contacts:
                            if self.viscord_window.contacts[contact]["button"].isOver((pygame.mouse.get_pos()[0],
                                                                                       pygame.mouse.get_pos()[1])):
                                if self.viscord_window.active_contact == contact:
                                    self.viscord_window.active_contact = None
                                    self.viscord_window.display_default_chat(display)
                                else:
                                    self.viscord_window.display_default_chat(display)
                                    self.viscord_window.active_contact = self.viscord_window.contacts[contact]
                                    self.viscord_window.display_contact_chat(contact, display)
                    if event.button == 3:
                        if self.terminal_window.active:
                            text = pygame.scrap.get(pygame.SCRAP_TEXT).decode("utf-8")[:-1]
                            if text:
                                self.terminal_window.active_input(display, text)

                if event.type == pygame.KEYDOWN:
                    if self.terminal_window.active:
                        self.terminal_window.active_input(display, event)

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

            if self.terminal:
                self.terminal_window.draw(display)
                self.terminal_window.move()
                if self.terminal_window.download_thread is not None and self.terminal_window.download_thread.is_alive() and not self.terminal_window.downloading:
                    self.terminal_window.download_thread.join()

        pygame.display.update()


class Versus:
    global display

    def __init__(self, game):
        self.socket = socket.socket()
        self.ip_input_box = button.InputBox(WIDTH / 2 - 100, HEIGHT / 2 - 100, 400, 50, BLACK, WHITE,
                                            pygame.font.SysFont("comicsansms", 30),
                                            "127.0.0.1:9999")  # "type: {IP Address:PORT}")
        self.name_input_box = button.InputBox(WIDTH / 2 - 100, HEIGHT / 2 - 50, 400, 50, BLACK, WHITE,
                                              pygame.font.SysFont("comicsansms", 30), "Player")
        self.game = game
        self.threads = []
        self.player_id = None
        self.name = "Player"

    def listen_to_server(self):
        while self.game.game_started:
            try:
                data = sr.recv_by_size(self.socket)
                if data:
                    t = threading.Thread(target=self.handle_data, args=(data,))
                    t.start()
                    self.threads.append(t)
            except:
                pass

    def connect(self, display):
        '''
        display connecting screen where the user can enter the ip address of the server and clicks connect
        :param display:
        :return:
        '''
        while True:
            display.fill(BG)
            connect_button = button.Button(WIDTH / 2 - 100, HEIGHT / 2 + 100, "Connect", BLACK, WHITE,
                                           pygame.font.SysFont("comicsansms", 30), True, GREEN, (200, 50))
            for event in pygame.event.get():
                self.ip_input_box.handle_event(event)
                self.name_input_box.handle_event(event)
                if event.type == pygame.QUIT:
                    self.game.state = "gameOver"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if connect_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                        try:
                            self.name = self.name_input_box.text
                            self.socket.connect((self.ip_input_box.text[:self.ip_input_box.text.find(':')],
                                                 int(self.ip_input_box.text[self.ip_input_box.text.find(':') + 1:])))
                            print("connected")
                            self.game.game_started = True
                            t = threading.Thread(target=self.listen_to_server)
                            self.threads.append(t)
                            t.start()
                            return
                        except:
                            pass
            self.name_input_box.update()
            self.name_input_box.render(display)
            self.ip_input_box.update()
            self.ip_input_box.render(display)
            self.game.EXIT_BUTTON.draw(display, pygame.mouse.get_pos())
            connect_button.draw(display, pygame.mouse.get_pos())
            pygame.display.update()

    def send_name(self):
        sr.send_with_size(self.socket, bytes("CONN~" + self.name, "utf-8"))

    def main_loop(self):
        while self.game.game_started:
            pygame.display.update()

    def handle_data(self, data):

        if data[:5] == b"NOBJ~":
            objective = pickle.loads(data[5:])
            self.game.objectives.add_existing_objective(objective)
            objective.set_game(self.game)
            objective.add_objective_to_contact(str(rnd.randint(1, 4)))
            return

        data_splitted = data.decode().split("~")
        message_code = data_splitted[0]

        if message_code == "COBJ":
            objective = self.game.objectives.get_objective_by_ip(data_splitted[1])
            self.game.terminal_window.write("File uploaded")
            objective.complete()
            self.game.completed_objectives.append(objective)
            self.game.objectives.remove(objective)

        if message_code == "FOBJ":
            objective = self.game.objectives.get_objective_by_ip(data_splitted[1])
            self.game.objectives.remove(objective)
            self.game.terminal_window.write("Task Failed")
            objective.fail()

        if message_code == "EOBJ":
            self.game.enemy_objectives_completed += 1

        if message_code == "STRT":
            self.game.game_started = True
            self.player_id = int(data_splitted[1])
            self.game.enemy_name = data_splitted[2]

        if message_code == "LOSE":
            self.game.state = "LOSE"
            self.game.game_started = False
            self.game.won = False

        if message_code == "WINN":
            self.game.state = "WIN"
            self.game.game_started = False
            self.game.won = True

        if message_code == "WAIT":
            self.send_name()

    def send_objective(self, file):
        sr.send_with_size(self.socket, b"SOBJ~" + str(self.player_id).encode() + b"~" + pickle.dumps(file))
        print("sent")


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
    def __init__(self, x, y, w, h, header_color, game):
        super().__init__(200, 100, w, h, "viscord", GREY20, header_color)
        self.game = game
        self.base_font = pygame.font.Font("assets/fonts/terminal.ttf", 14)
        self.sided_menu = pygame.rect.Rect(self.x, self.y + self.header_rect.height, 250,
                                           self.h - self.header_rect.height)
        self.rects.append(self.sided_menu)
        self.contact_chat_rect = pygame.rect.Rect(self.sided_menu.topright[0], self.sided_menu.top,
                                                  self.application.right - self.sided_menu.right - 3,
                                                  self.application.bottom - self.header_rect.bottom - 3)
        self.help_contact = button.Button(self.sided_menu.bottomleft[0] + 3,
                                          self.sided_menu.bottomleft[1] - 50, "HELP", BLACK, WHITE,
                                          self.header_font, False, GREEN, (244, 47))
        self.rects.append(self.contact_chat_rect)
        self.buttons.append(self.help_contact)
        self.contacts = {}
        self.contact1 = button.Button(self.sided_menu.topleft[0] + 3, self.sided_menu.topleft[1] + 3, "H04X", WHITE, BG,
                                      self.header_font, False, BLACK, (244, 47))
        self.contacts["1"] = {"button": self.contact1, "chat": "", "name": "H04X", "objectives": []}
        self.contact2 = button.Button(self.sided_menu.topleft[0] + 3,
                                      self.sided_menu.topleft[1] + 3 + 47, "4L4K4Z4M", WHITE, BG,
                                      self.header_font, False, BLACK, (244, 47))
        self.contacts["2"] = {"button": self.contact2, "chat": "", "name": "4L4K4Z4M", "objectives": []}
        self.contact3 = button.Button(self.sided_menu.topleft[0] + 3,
                                      self.sided_menu.topleft[1] + 3 + 47 * 2, "FL45H", WHITE, BG,
                                      self.header_font, False, BLACK, (244, 47))
        self.contacts["3"] = {"button": self.contact3, "chat": "", "name": "FL45H", "objectives": []}
        self.contact4 = button.Button(self.sided_menu.topleft[0] + 3,
                                      self.sided_menu.topleft[1] + 3 + 47 * 3, "CH405", WHITE, BG,
                                      self.header_font, False, BLACK, (244, 47))
        self.contacts["4"] = {"button": self.contact4, "chat": "", "name": "CH405", "objectives": []}
        self.active_contact = None

    def draw(self, display):
        super().draw(display)
        pygame.draw.rect(display, BLACK, self.sided_menu, 3)
        pygame.draw.rect(display, GREY20, self.contact_chat_rect)
        for i in range(len(self.contacts)):
            self.contacts[str(i + 1)]["button"].draw(display, pygame.mouse.get_pos())
        self.help_contact.draw(display, pygame.mouse.get_pos())
        if self.active_contact is not None:
            self.display_contact_chat(self.active_contact, display)

    def move(self):
        super().move()
        if pygame.mouse.get_pressed()[0]:
            if self.header_rect.collidepoint(pygame.mouse.get_pos()):
                self.sided_menu.x = self.x
                self.sided_menu.y = self.y + self.header_rect.height
                self.contact_chat_rect.x = self.sided_menu.topright[0]
                self.contact_chat_rect.y = self.sided_menu.top
                self.help_contact.x = self.sided_menu.bottomleft[0] + 3
                self.help_contact.y = self.sided_menu.bottomleft[1] - 50
                for i in range(len(self.contacts)):
                    self.contacts[str(i + 1)]["button"].x = self.sided_menu.topleft[0] + 3
                    self.contacts[str(i + 1)]["button"].y = self.sided_menu.topleft[1] + 3 + 47 * i
                if self.active_contact is not None:
                    self.display_contact_chat(self.active_contact, display)

    def display_contact_chat(self, contact, display):

        self.contact_chat_rect.y = self.sided_menu.top
        self.contact_chat_rect.height = self.application.bottom - self.header_rect.bottom - 3

        if type(contact) is str:
            chat = self.contacts[contact]["chat"]
        else:
            chat = contact["chat"]

        from_contact = []
        for message in chat.split("\n"):
            from_contact.append(message)

        if len(from_contact) > 0:
            for message in from_contact:
                # check if the size of the rendered message is too long to fit in the chat box and if so, split it into multiple lines (text wrapping) then display the messages
                if self.base_font.size(message)[0] > self.contact_chat_rect.width - 3:
                    words = message.split(" ")
                    line = ""
                    lines = []
                    for word in words:
                        if self.base_font.size(line + word)[0] > self.contact_chat_rect.width - 3:
                            lines.append(line)
                            line = ""
                        line += " " + word
                    lines.append(line)
                    for line in lines:
                        display.blit(self.base_font.render(line, True, WHITE),
                                     (self.contact_chat_rect.x, self.contact_chat_rect.y))
                        self.contact_chat_rect.y += self.base_font.size(line)[1] + 5
                        self.contact_chat_rect.height -= self.base_font.size(line)[1] + 5

                else:
                    display.blit(self.base_font.render(message, True, WHITE),
                                 (self.contact_chat_rect.x, self.contact_chat_rect.y))
                    self.contact_chat_rect.y += self.base_font.size(message)[1] + 5
                    self.contact_chat_rect.height -= self.base_font.size(message)[1] + 5
                self.contact_chat_rect.y += 15
                self.contact_chat_rect.height -= 15

            # check if the chat is full and if so, scroll down
            if self.contact_chat_rect.height < 0:
                self.contact_chat_rect.y = self.sided_menu.top
                self.contact_chat_rect.height = self.application.bottom - self.header_rect.bottom - 3
                if type(contact) is str:
                    self.contacts[contact]["chat"] = ""
                else:
                    contact["chat"] = ""

    def display_default_chat(self, display):
        self.contact_chat_rect = pygame.rect.Rect(self.sided_menu.topright[0], self.sided_menu.top,
                                                  self.application.right - self.sided_menu.right - 3,
                                                  self.application.bottom - self.header_rect.bottom - 3)
        pygame.draw.rect(display, LIGHT_SKY_BLUE_4, self.contact_chat_rect)


class Terminal(Application):
    def __init__(self, x, y, w, h, header_color, game):
        super().__init__(x, y, w, h, "terminal", BLACK, header_color)
        self.connected = False
        self.game = game
        self.input_rect = pygame.rect.Rect(self.x, self.header_rect.bottom, self.w,
                                           self.application.height - self.header_rect.height)
        self.rects.append(self.input_rect)
        self.user_text = r'root@CoolHacker:~$ '
        self.base_font = pygame.font.Font("assets/fonts/terminal.ttf", 14)
        self.input_text = self.base_font.render(self.user_text, True, WHITE)
        self.IO_rect = pygame.rect.Rect(self.input_rect)
        self.active = False
        self.input = ""
        self.history = []
        self.linebreak = 0
        self.active_objective = None
        self.display = display
        self.downloading = False
        self.download_thread = None
        self.folder = []
        self.versus = None

    def draw(self, display):
        super().draw(display)
        pygame.draw.rect(display, BLACK, self.input_rect)
        for item in self.history:
            text = self.base_font.render(item[0], True, WHITE)
            display.blit(text, (item[2] + 5, item[1] + 5))
        display.blit(self.input_text, (self.input_rect.x + 5, self.input_rect.y + 5))
        pygame.display.update()

    def move(self):
        super().move()
        if pygame.mouse.get_pressed()[0]:
            if self.header_rect.collidepoint(pygame.mouse.get_pos()):
                tmp = self.IO_rect.y
                self.IO_rect.x = self.x
                self.IO_rect.y = self.y + self.header_rect.height
                self.input_rect.x = self.x
                self.input_rect.y = self.IO_rect.y + 30 * self.linebreak
                new_history = []
                for item in self.history:
                    item = (item[0], self.IO_rect.y + (abs(tmp - item[1])), self.x)
                    new_history.append(item)
                self.history = new_history

    def active_input(self, display, event):
        if not self.downloading:
            if type(event) == str:
                self.user_text += event
            elif event.key == pygame.K_BACKSPACE:
                if len(self.user_text) > len("root@CoolHacker:~$ "):
                    self.user_text = self.user_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.input = self.user_text[len("root@CoolHacker:~$ "):]
                self.history.append(((self.user_text), self.input_rect.y, self.input_rect.x))
                self.linedown()
                self.input_rect.y = self.IO_rect.y + 30 * self.linebreak
                self.input_rect.height = self.input_rect.height - 30
                self.user_text = "root@CoolHacker:~$ "
                self.handle_input(display)
            else:
                self.user_text += event.unicode
            self.input_text = self.base_font.render(self.user_text, True, WHITE)
            pygame.draw.rect(display, BLACK, self.input_rect)
            display.blit(self.input_text, (self.x + 5, self.input_rect.y + 5))
            pygame.display.update()

    def handle_input(self, display):
        input = self.input
        self.input = ""
        if self.connected:
            if input == "":
                pass
            elif input == "exit":
                self.connected = False
                self.write("Disconnected")
            elif input == "ls":
                self.print_folders()
            elif input[:3] == "ls " and input[3:] in self.active_objective.get_folders_names():
                self.print_folder_contents(input[3:])
            elif input[:4] == "cat " and input[
                                         4:input.find('/')] in self.active_objective.get_folders_names() and input[
                                                                                                             input.find(
                                                                                                                 '/') + 1:] in \
                    self.active_objective.folders[input[4:input.find('/')]].get_folder_contents():
                self.print_file_contents(input[4:input.find('/')], input[input.find('/') + 1:])
            elif input[:4] == "get " and input[
                                         4:input.find('/')] in self.active_objective.get_folders_names() and input[
                                                                                                             input.find(
                                                                                                                 '/') + 1:] in \
                    self.active_objective.folders[input[4:input.find('/')]].get_folder_contents():
                self.download_thread = threading.Thread(target=self.get_file,
                                                        args=(input[4:input.find('/')], input[input.find('/') + 1:]))
                self.download_thread.start()
                self.folder.append(
                    self.active_objective.folders[input[4:input.find('/')]].files[input[input.find('/') + 1:]])
            else:
                self.write("Command not found")
        else:
            if input == "":
                return
            elif input[:5] == "nmap " and input[5:] in self.game.objectives.get_objectives_ips():
                self.nmap(input[5:])
            elif input[:len("smb445exploit ")] == "smb445exploit " and input[
                                                                       len("smb445exploit "):] in self.game.objectives.get_objectives_ips():
                self.connect(input[len("smb445exploit "):])
            elif input[:len("http80exploit ")] == "http80exploit " and input[
                                                                       len("http80exploit "):] in self.game.objectives.get_objectives_ips():
                self.connect(input[len("http80exploit "):])
            elif input[:len("ftp21exploit ")] == "ftp21exploit " and input[
                                                                     len("ftp21exploit "):] in self.game.objectives.get_objectives_ips():
                self.connect(input[len("ftp21exploit "):])
            elif input[:len("ssh22exploit ")] == "ssh22exploit " and input[
                                                                     len("ssh22exploit "):] in self.game.objectives.get_objectives_ips():
                self.connect(input[len("ssh22exploit "):])
            elif input[:2] == "ls":
                for item in self.folder:
                    self.write(str(item.name))
            elif input[:4] == "cat ":
                for item in self.folder:
                    if item.name == input[4:]:
                        self.write(item.content)
            elif input[:7] == "upload ":
                for contact in self.game.viscord_window.contacts:
                    if self.game.viscord_window.contacts[contact]["name"] == input[7:input.rfind(' ')]:
                        for item in self.folder:
                            if item.name == input[input.rfind(' ') + 1:]:
                                for objective in self.game.viscord_window.contacts[contact]["objectives"]:
                                    if objective.target_file.name == item.name and objective.target_file.content == item.content:
                                        if not self.game.online:
                                            objective.complete()
                                            self.write("File uploaded")
                                            self.folder.remove(item)
                                        else:
                                            self.versus.send_objective(item)
                                            self.folder.remove(item)

            else:
                self.write("Command not found")
                print()

    def nmap(self, input):
        self.history.append(((self.user_text), self.input_rect.y, self.input_rect.x))
        self.linedown()

        self.history.append(("Nmap version 7.40 ( http://nmap.org )", self.input_rect.y, self.x))
        self.linedown()
        self.history.append(("Nmap scan report for " + input, self.input_rect.y, self.x))
        self.linedown()
        self.history.append(("Host is up", self.input_rect.y, self.x))
        self.linedown()
        self.history.append(("PORT    STATE SERVICE", self.input_rect.y, self.x))
        self.linedown()
        self.history.append((self.game.objectives.get_objective_by_ip(input).service, self.input_rect.y, self.x))
        self.linedown()

    def connect(self, input):
        self.connected = True
        self.active_objective = self.game.objectives.get_objective_by_ip(input)
        print(self.active_objective.get_folders_names())
        self.clear_console()
        self.write("Connecting to " + input)
        time.sleep(1)
        self.write("Connection Established")
        time.sleep(1)
        self.linedown()
        self.print_folders()

    def write(self, text):
        self.history.append(((text), self.input_rect.y, self.x))
        self.linedown()
        self.draw(self.display)

    def get_file(self, folder, file):
        self.downloading = True
        self.clear_console()
        self.write("Downloading " + file + " from " + folder)
        self.user_text = "----------------------------------------"
        for i in range(len(self.user_text)):
            self.user_text = self.user_text[:i] + "#" + self.user_text[i + 1:]
            time.sleep(rnd.uniform(0, 0.5))
            self.input_text = self.base_font.render(self.user_text, True, WHITE)
            display.blit(self.input_text, (self.x + 5, self.input_rect.y + 5))
            pygame.display.update()
        self.write("Download complete")
        self.linedown()
        self.user_text = "root@CoolHacker:~$ "
        self.downloading = False

    def print_folders(self):
        for item in self.active_objective.get_folders_names():
            self.write(str(item))

    def print_folder_contents(self, folder):
        for item in self.active_objective.folders[folder].get_folder_contents():
            self.write(str(item))

    def print_file_contents(self, folder, file):
        self.write(self.active_objective.folders[folder].files[file].content)

    def linedown(self, input=None, space=30):
        self.linebreak += 1
        self.input_rect.y = self.IO_rect.y + space * self.linebreak
        self.input_rect.height = self.input_rect.height - space
        if self.input_rect.y >= self.application.bottom:
            self.input_rect.y = self.IO_rect.y
            self.linebreak = 0
            self.input_rect.height = self.application.height - self.header_rect.height
            self.history = []

    def clear_console(self):
        self.history = []
        self.linebreak = 0
        self.input_rect.y = self.IO_rect.y


def genIPv4():
    ip = str(
        str(rnd.randint(172, 192)) + "." + str(rnd.randint(0, 255)) + "." + str(
            rnd.randint(0, 255)) + "." + str(
            rnd.randint(1, 255)))
    return ip


class Objectives:
    def __init__(self, game):
        self.game = game
        self.objectives = []

    def get_objectives_ips(self):
        ips = []
        for item in self.objectives:
            ips.append(item.ip)
        return ips

    def get_objective_by_ip(self, ip):
        for item in self.objectives:
            if item.ip == ip:
                return item
        return None

    def add_objective(self, contact):
        to_add = Objective()
        to_add.set_game(self.game)
        self.objectives.append(to_add)
        to_add.add_objective_to_contact(contact)

    def add_existing_objective(self, objective):
        self.objectives.append(objective)


class Objective:
    def __init__(self):
        self.ip = genIPv4()
        self.open_service = rnd.randint(0, 3)
        # 0 = ssh, 1 = http, 2 = smb, 3 = ftp
        if self.open_service == 0:
            self.service = "22/tcp open  ssh"
        if self.open_service == 1:
            self.service = "80/tcp open  http"
        if self.open_service == 2:
            self.service = "445/tcp open  smb"
        if self.open_service == 3:
            self.service = "21/tcp open  ftp"
        self.completed = False
        self.game = None
        self.folders = {}
        self.contact = None
        self.folders_amount = rnd.randint(1, 5)
        for i in range(self.folders_amount):
            folder = Folder()
            folder_name = folder.name
            while folder.name in self.folders.keys():
                folder = Folder()
            self.folders[folder_name] = folder
        # select a random folder to put the objective file in
        random_folder = list(self.folders.keys())[rnd.randint(0, len(self.folders) - 1)]
        self.target_file = File(RANDOM_WORDS_LIST[rnd.randint(0, len(RANDOM_WORDS_LIST) - 1)] + ".txt",
                                "This is the objective file")
        self.folders[random_folder].add_existing_file(self.target_file)

    def set_game(self, game):
        self.game = game

    def complete(self):
        self.game.money += rnd.randint(60, 120)
        self.game.objectives.objectives.remove(self)
        self.game.viscord_window.contacts[self.contact]["chat"] += "Task Completed (" + str(self.ip) + ") \n"
        self.game.viscord_window.contacts[self.contact]["objectives"].remove(self)

    def fail(self):
        self.completed = True
        self.game.viscord_window.contacts[self.contact]["chat"] += "Task Failed (" + str(self.ip) + ") \n"
        self.game.viscord_window.contacts[self.contact]["objectives"].remove(self)
        self.game.objectives.objectives.remove(self)

    def get_folders_names(self):
        names = []
        for item in self.folders.keys():
            names.append(item)
        return names

    def check_if_objective_completed(self, file):
        if file.__dict__ == self.target_file.__dict__:
            return True
        return False

    def add_objective_to_contact(self, contact):
        self.game.viscord_window.contacts[
            contact][
            "chat"] += "Hey there, Can you help me get a file that contains the text \"This is the RIGHT FILE\" from " \
                       "the ip: " + self.ip + "?\n "
        self.game.viscord_window.contacts[contact]["objectives"].append(self)
        self.contact = contact


class Folder:
    def __init__(self):
        self.name = RANDOM_WORDS_LIST[rnd.randint(0, len(RANDOM_WORDS_LIST) - 1)]
        self.files = {}
        self.files_amount = rnd.randint(0, 3)
        for i in range(self.files_amount):
            file = File()
            file_name = file.name
            while file.name in self.files.keys():
                file = File()
            self.files[file_name] = file

    def get_folder_contents(self):
        contents = []
        for item in self.files.keys():
            contents.append(item)
        return contents

    def add_file(self, file_name, file_content):
        self.files[file_name] = File(file_name, file_content)

    def add_existing_file(self, file):
        self.files[file.name] = file


class File:
    def __init__(self, name=None, content=None):
        if name is None:
            self.name = RANDOM_WORDS_LIST[rnd.randint(0, len(RANDOM_WORDS_LIST) - 1)] + ".txt"
        else:
            self.name = name
        # super random content
        if content is None:
            self.content = ""
            for i in range(rnd.randint(0, 10)):
                self.content += RANDOM_WORDS_LIST[rnd.randint(0, len(RANDOM_WORDS_LIST) - 1)] + " "
        else:
            self.content = content


def genIPv4():
    ip = str(str(rnd.randint(172, 192)) + "." + str(rnd.randint(0, 255)) + "." + str(
        rnd.randint(0, 255)) + "." + str(
        rnd.randint(1, 255)))
    return ip


# main_loop
def main():
    global display
    global ARIAL_FONT
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.scrap.init()
    clock = pygame.time.Clock()
    ARIAL_FONT = pygame.font.SysFont("arial", 25)

    game = GameStates()
    # Main game loop
    running = True
    while running:
        game.state_manager()
        clock.tick(REFRESH_RATE)


if __name__ == '__main__':
    main()
