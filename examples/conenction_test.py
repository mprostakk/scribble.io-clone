import socket
from threading import Thread


host = 'localhost'
port = 1781


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


def worker():
    while True:
        buffer = s.recv(100)
        print(buffer)


worker_thread = Thread(target=worker)
worker_thread.daemon = True
worker_thread.start()


while True:
    x = input('Action: ')
    d = input('Data:')
    u = input('User')
    send_handshake = f'Action: {x}\r\nData: {"{"}"message": "{d}"{"}"}\r\nUser: {u}\r\n\r\n'
    s.sendall(send_handshake.encode('utf-8'))


# send_data = 'Action: DRAW\r\nHeaders-Length: 2\r\nContent-Length: 43\r\nData: 1.0, 2.2\r\n\r\n'
# s.sendall(send_data.encode('utf-8'))
