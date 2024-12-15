from socket import socket
from threading import Thread

from controller.enc_socket import EncryptedSocket


class ClientHandler(Thread):
    def __init__(self, socket: socket):
        Thread.__init__(self)
        self.socket = socket

    def run(self):
        self.socket = EncryptedSocket(self.socket)







