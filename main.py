import socket

import controller

if __name__ == '__main__':
    server = socket.socket()
    server.bind(("0.0.0.0", 4567))
    server.listen()
    T = []
    while True:
        client, addr = server.accept()
        c_h = controller.ClientHandler(client)
        T.append(c_h)
        c_h.start()

    for i in T:
        i.join()


