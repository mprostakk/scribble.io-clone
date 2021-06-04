import typing as tp

from custom_request import Request


class CustomClient:
    def __init__(self, client, username):
        self.client = client
        self.username = username


class CustomClients:
    def __init__(self):
        self.d = {
            # 'username': CustomClient
        }

    def add_client(self, client, username):
        self.d[username] = client

    def username_to_client(self):
        pass

    def remove_client(self, client):
        pass

    def remove_client_by_username(self, username):
        pass

    def get_clients(self):
        pass


def read(client, sepp='\r\n'):
    buffer = client.recv(1).decode('utf-8')

    while not (sepp in buffer):
        data = client.recv(1).decode('utf-8')
        buffer += data

    return buffer[:len(buffer)-2]


def receive(client):
    data = b''
    while b'\r\n\r\n' not in data:
        data += client.recv(1)

    data = data.decode('utf-8')
    return data


def receive_request(client) -> Request:
    rcv_data = receive(client)
    request = Request()
    request.parse_request(rcv_data)
    return request
