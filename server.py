# server for the game
import pickle
import socket
import sys
import threading
import time
import random
from utils import tcp_by_size as sr
import datetime
import wx
from utils.colors import *
from main import Objective, Objectives, Folder, File

HEIGHT = 500
WIDTH = 300

IP = "127.0.0.1"
PORT = 9999
DEBUG = True


class MyButtons(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(WIDTH, HEIGHT))

        wx.Button(self, 1, "Start", pos=(WIDTH//2 - 110//2, 0), size=(110, -1))
        wx.Button(self, 2, "Close", pos=(WIDTH//2 - 110//2, 30),size=(110, -1))

        self.log = wx.TextCtrl(self, wx.ID_ANY, pos=(0, 170), size=(284, HEIGHT - 209),
                               style=wx.TE_READONLY | wx.TE_MULTILINE | wx.ALIGN_LEFT | wx.TE_LEFT)



        self.Bind(wx.EVT_BUTTON, self.on_start, id=1)
        self.Bind(wx.EVT_BUTTON, self.on_close, id=2)

        sys.stdout = self.log

        self.Centre()
        self.ShowModal()

    def on_start(self, event):
        server = Server()
        server.start_listen()

    def on_close(self, event):
        self.Close(True)
        self.Destroy()


class Server:
    def __init__(self):
        self.srv_socket = socket.socket()
        self.srv_socket.bind(('0.0.0.0', 9999))
        self.srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.players = {}
        self.players_data = []
        self.threads = []
        self.objectives_sent = []
        self.sent_all = False
        self.completed_objectives = {}

    def start_listen(self):
        print("Server started")
        self.srv_socket.listen(2)

        thread = threading.Thread(target=self.accept_clients)
        self.threads.append(thread)
        thread.start()

    def start_game(self):
        print("Game started")
        names = self.recv_names()
        print("Got Names")
        self.players_data = names
        for tup in names:
            sock = tup[1]
            name = tup[2]
            other_name = names[0][2] if names[0][1] != sock else names[1][2]
            player_id = tup[0]
            self.send_start(sock, player_id, other_name)
        t = threading.Thread(target=self.send_objective)
        self.threads.append(t)
        t.start()
        t = threading.Thread(target=self.game_loop)
        self.threads.append(t)
        t.start()

    def game_loop(self):
        t = threading.Thread(target=self.recv_data, args=(self.players[self.players_data[0][1]],))
        self.threads.append(t)
        t.start()
        t = threading.Thread(target=self.recv_data, args=(self.players[self.players_data[1][1]],))
        self.threads.append(t)
        t.start()
        while True:
            pass

    def recv_data(self, sock):
        while True:
            try:
                data = sr.recv_by_size(sock)

                if data:
                    t = threading.Thread(target=self.handle_data, args=(data, sock))
                    self.threads.append(t)
                    t.start()
            except:
                pass

    def handle_data(self, data, sock):
        if data:
            player_id = data.decode('utf-8').split('~')[1]
            if data.decode('utf-8').startswith('SOBJ'):
                player_id = int(data.decode('utf-8').split('~')[1])
                file = pickle.loads(data.split('~')[2])
                self.check_file(file, player_id, sock)

            else:
                print(data.decode('utf-8'))

    def check_file(self, file, player_id, sock):
        objective = None
        for objective in self.objectives_sent:
            if objective.target_file.check_file(file):
                self.completed_objectives[player_id] = objective
                self.objectives_sent.remove(objective)
                sr.send_with_size(sock, b'COBJ~' + str(objective.ip).encode('utf-8'))
                # send the other player message code "EOBJ"
                for player in self.players:
                    if player != sock:
                        sr.send_with_size(player, b'EOBJ~' + str(objective.ip).encode('utf-8'))
                return
        sr.send_with_size(sock, b'FOBJ')

    def send_start(self, sock, player_id, other_name):
        sr.send_with_size(sock, b'STRT~' + str(player_id).encode('utf-8') + b'~' + other_name.encode('utf-8'))

    def recv_names(self):
        names = []
        for sock in self.players:
            data = sr.recv_by_size(sock)
            if data:
                if data.decode('utf-8').startswith('CONN'):
                    name = data.decode('utf-8').split('~')[1]
                    names.append((self.players[sock], sock, name))
        return names

    def send_objective(self):

        while True:
            objective = Objective()
            to_send = pickle.dumps(objective)
            code = b'NOBJ~'
            for player in self.players_data:
                sr.send_with_size(player[1], code + to_send)
            self.objectives_sent.append(objective)
            if len(self.objectives_sent) == 10:
                self.sent_all = True
                break
            time.sleep(30)

    def accept_clients(self):
        print("Waiting for clients...")
        while True:
            try:
                client_sock, addr = self.srv_socket.accept()
                player_id = len(self.players)
                self.players[client_sock] = player_id
                print("Client connected from: " + str(addr))
                if len(self.players) == 2:
                    print("Two players connected\n")
                    self.send_wait()
                    self.start_game()
                    break
            except:
                pass

    def send_wait(self):
        for sock in self.players:
            sr.send_with_size(sock, b'WAIT~')


def main():

    app = wx.App(0)
    MyButtons(None, -1, 'server.py')
    app.MainLoop()




if __name__ == '__main__':
    main()









