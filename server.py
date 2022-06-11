# server for the game

import socket
import sys
import threading
import time
import random
from utils import tcp_by_size as sr
import datetime
import wx
from utils.colors import *

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
        server.start()

    def on_close(self, event):
        self.Close(True)
        self.Destroy()

class Server():
    def __init__(self):
        self.srv_socket = socket.socket()
        self.srv_socket.bind(('0.0.0.0', 9999))
        self.srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.players = []
        self.threads = []

    def start(self):
        print("Server started")
        self.srv_socket.listen(2)

        thread = threading.Thread(target=self.accept_clients)
        self.threads.append(thread)
        thread.start()

    def accept_clients(self):
        print("Waiting for clients...")
        while True:
            try:
                client_sock, addr = self.srv_socket.accept()
                self.players.append(client_sock)
                self.text_box.AppendText("Client connected from: " + str(addr))
                self.text_box.AppendText("\n")
                if len(self.players) == 2:
                    self.text_box.AppendText("Two players connected\n")
                    break
            except:
                pass


def main():

    app = wx.App(0)
    MyButtons(None, -1, 'server.py')
    app.MainLoop()




if __name__ == '__main__':
    main()









