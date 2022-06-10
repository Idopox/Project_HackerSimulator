# Author: Ido Barkan
# Hacker Simulator Game - Project
import random as rnd
import sys
import time

import pygame
from pygame import mixer

from utils import button
from utils.colors import *
import threading

WIDTH = 1920
HEIGHT = 1080
REFRESH_RATE = 60
BG = LIGHT_BLUE_4
DEFAULT_VOL = 0
RANDOM_WORDS_LIST = ["ink", "historical", "caption", "medical", "garrulous", "snakes", "lake", "pour", "mountainous",
                     "cactus", "extra-small", "rake", "apple", "jar", "drop",
                     "tiger", "tired", "toy"]
SERVICES = ["http", "ssh", "ftp", "smb"]
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.scrap.init()
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
        self.viscord_window = Viscord(WIDTH / 2 + 150, HEIGHT / 2 - 500, 800, 700, LIGHT_GREY, self)
        self.terminal_window = Terminal(WIDTH / 2 + 150, HEIGHT / 2 - 500, 800, 700, LIGHT_GREY, self)
        self.objectives = Objectives(self)
        self.objectives.add_objective()
        print(self.objectives.objectives[0].ip)

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
    def __init__(self, x, y, w, h, header_color, game):
        super().__init__(x, y, w, h, "viscord", GREY20, header_color)
        self.game = game
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
        self.contacts = []

    def draw(self, display):
        super().draw(display)
        pygame.draw.rect(display, BLACK, self.sided_menu, 3)
        pygame.draw.rect(display, LIGHT_SKY_BLUE_4, self.contact_chat_rect)
        self.help_contact.draw(display, pygame.mouse.get_pos())
        pygame.display.update()

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
            else:
                self.write("Command not found")

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
        self.download_thread.join()

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

    def add_objective(self):
        self.objectives.append(Objective(self.game))


class Objective:
    def __init__(self, game):
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
        self.game = game
        self.folders = {}
        self.folders_amount = rnd.randint(1, 5)
        for i in range(self.folders_amount):
            folder = Folder()
            folder_name = folder.name
            while folder.name in self.folders.keys():
                folder = Folder()
            self.folders[folder_name] = folder
        print(self.folders_amount)
        i = rnd.randint(0, self.folders_amount - 1)
        print(i)
        print(list(self.folders.keys()))
        self.folders[list(self.folders.keys())[i]].files["objective.txt"] = File("objective.txt")

    def complete(self):
        self.completed = True
        self.game.money += rnd.randint(60, 120)
        self.game.objectives.remove(self)

    def get_folders_names(self):
        names = []
        for item in self.folders.keys():
            names.append(item)
        return names


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


class File:
    def __init__(self, name=None, content=None):
        if name == "objective.txt":
            self.name = "mystery.txt"
            self.content = "YOU HAVE FOUND THE RIGHT FILE"
        else:
            self.name = RANDOM_WORDS_LIST[rnd.randint(0, len(RANDOM_WORDS_LIST) - 1)] + ".txt"
            # super random content
            self.content = ""
            for i in range(rnd.randint(0, 10)):
                self.content += RANDOM_WORDS_LIST[rnd.randint(0, len(RANDOM_WORDS_LIST) - 1)] + " "


def genIPv4():
    ip = str(str(rnd.randint(172, 192)) + "." + str(rnd.randint(0, 255)) + "." + str(
        rnd.randint(0, 255)) + "." + str(
        rnd.randint(1, 255)))
    return ip


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
