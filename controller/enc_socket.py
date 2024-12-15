from socket import socket
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from collections.abc import Buffer
from Crypto import Random

from Crypto.SelfTest.Signature.test_pss import public_key

BLOCK_SIZE = 2 ** 4

class EncryptedSocket:

    def __init__(self, socket: socket):
        self.socket = socket
        rsa = RSA.generate(2048)
        socket.send(rsa.public_key().export_key())
        sym_key = socket.recv(1024)
        cipher = PKCS1_OAEP.new(rsa)
        sym_key = cipher.decrypt(sym_key)
        self.cipher = AES.new(sym_key, AES.MODE_ECB)

    def send(self, data: Buffer):
        peding = (BLOCK_SIZE - len(data) & (BLOCK_SIZE - 1)) & (BLOCK_SIZE - 1)
        data += b"\0" * peding
        return self.socket.send(self.cipher.encrypt(data))

    def recv(self, bufsize: int):
        data = self.socket.recv(bufsize)
        return self.cipher.decrypt(data).rstrip(b"\0")


class EncSocketClient:

    def __init__(self, host, port):
        self.socket = socket()
        self.socket.connect((host, port))
        public_key = self.socket.recv(1024)
        rsa = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa)
        rand = Random.new()
        self.cipher = AES.new(aes:=rand.read(BLOCK_SIZE), AES.MODE_ECB)
        self.socket.send(cipher.encrypt(aes))

    def send(self, data: Buffer):
        peding = (BLOCK_SIZE - len(data) & (BLOCK_SIZE - 1)) & (BLOCK_SIZE - 1)
        data += b"\0" * peding
        return self.socket.send(self.cipher.encrypt(data))

    def recv(self, bufsize: int):
        data = self.socket.recv(bufsize)
        return self.cipher.decrypt(data).rstrip(b"\0")




