# server for the game

import socket
import sys
import threading
import time
import random
from assets import tcp_by_size as sr
import datetime

IP = "127.0.0.1"
PORT = 9999
DEBUG = True
all_to_die = False


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


def main():
    global all_to_die
    threads = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.listen(2)
    print("Server started on port " + str(PORT))

    running = True
    i = 1
    while running:
        player_sock, addr = s.accept()
        print("Connection from " + str(addr))
        t = threading.Thread(target=handle_player, args=(player_sock, addr, i))
        t.start()
        i += 1
        threads.append(t)
    all_to_die = True
    for t in threads:
        t.join()
    s.close()



if __name__ == '__main__':
    main()









