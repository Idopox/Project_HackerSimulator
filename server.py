# server for the game

import socket
import sys
import threading
import time
import random
from utils import tcp_by_size as sr
import datetime
import pygame
from utils import button
from utils.colors import *

HEIGHT = 600
WIDTH = 800

IP = "127.0.0.1"
PORT = 9999
DEBUG = True
all_to_die = False
threads = []

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Server")



def log(data, direction):
    if direction == 'recv':
        print('=============\nTime: %s \nRecived from Client To Server>>> %s <<<\n=============' % (datetime.datetime.now().strftime('%Y%m%d %H:%M'), data))
    elif direction == 'sent':
        print('=============\nTime: %s \nSent from Server To Client>>> %s <<<\n=============' % (datetime.datetime.now().strftime('%Y%m%d %H:%M'), data))


def recv_data(sock):
    data = sr.recv_by_size(sock)
    if data:
        if DEBUG:
            log(data, 'recv')
        return data.decode()


def handle_player(player_sock, addr, i):
    global all_to_die
    while not all_to_die:
        data = recv_data(player_sock)
        if data:
            t = threading.Thread(target=handle_player_data, args=(player_sock, addr, data))
        else:
            pass
    print("Thread " + str(i) + " closed")

def run_server():
    global threads
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((IP, PORT))
    server_sock.listen(2)
    print("Server started on port " + str(PORT))
    i = 1
    while not all_to_die:
        player_sock, addr = server_sock.accept()
        print("Player number " + str(i) + " connected from address: " + str(addr))
        t = threading.Thread(target=handle_player, args=(player_sock, addr, i))
        threads.append(t)
        t.start()
        i += 1

def main():
    global all_to_die
    global threads
    font = pygame.font.SysFont('Arial', 30)
    start_server_button = button.Button(WIDTH / 2, HEIGHT / 2, 'Start Server', BLACK,WHITE, font, True, GREEN)
    running = True
    run_server = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_server_button.isOver((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])):
                    all_to_die = False
                    run_server = True
        display.fill(WHITE)
        start_server_button.draw(display, pygame.mouse.get_pos())
        pygame.display.update()
        if run_server:
            t = threading.Thread(target=run_server)




if __name__ == '__main__':
    main()









