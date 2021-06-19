import typing as tp
from uuid import uuid4
from custom_request import Request


class CustomClients:
    def __init__(self):
        self.d = dict()
        self.sessions = dict()

    def add_client(self, client, username):
        self.d[username] = client

        session_id = self.init_session_id()
        while self.is_session_id_taken(session_id):
            session_id = self.init_session_id()

        self.sessions[username] = session_id

    def is_session_id_taken(self, session_id) -> bool:
        for key, value in self.sessions.items():
            if value == session_id:
                return True
        
        return False

    def get_session_id(self, username):
        return self.sessions.get(username)

    def init_session_id(self):
        return uuid4()

    def username_to_client(self, username):
        return self.d.get(username)

    def client_to_username(self, client):
        for key, value in self.d.items():
            if value == client:
                return key

        return None

    def remove_client(self, client):
        username = None
        for key, value in self.d.items():
            if value == client:
                username = key
                break

        if username is not None:
            self.d.pop(username)

    def remove_client_by_username(self, username) -> None:
        self.d.pop(username)

    def get_all_clients(self) -> tp.List:
        clients = list()
        for key, value in self.d.items():
            clients.append(value)

        return clients

    def get_clients_from_request(self, request) -> tp.List:
        users: list = request.to_users

        if len(users):
            clients = list()
            for user in users:
                clients.append(self.username_to_client(user))

            return clients

        return self.get_all_clients()

    def get_all_usernames(self) -> tp.List:
        return [username for username, _ in self.d.items()]


RECV_LEN = 1


def read(client, sepp='\r\n'):
    buffer = client.recv(RECV_LEN).decode('utf-8')

    while not (sepp in buffer):
        data = client.recv(RECV_LEN).decode('utf-8')
        buffer += data

    return buffer[:len(buffer)-2]


def receive(client):
    data = b''
    while b'\r\n\r\n' not in data:
        data += client.recv(RECV_LEN)

    data = data.decode('utf-8')
    return data


def receive_request(client) -> Request:
    rcv_data = receive(client)
    request = Request()
    request.parse_request(rcv_data)
    return request
