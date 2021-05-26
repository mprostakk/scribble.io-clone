
from functools import update_wrapper
import socket
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


host = 'localhost'
port = 1781


class Request:
    def __init__(self):
        self.headers = dict()
    
    def parse_request(self, data: str) -> None:
        stripped_data = data[:-2].split('\r\n')
        for header in stripped_data:
            if header == '':
                continue

            name, data = header.split(': ')
            self.headers[name] = data

class ServerBase:

    def __init__(self) -> None:
        self.buffer = []
        logging.info('Creating socket')
        self.number_of_clients = 2  
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(self.number_of_clients)
        logging.info(f'Listening to {self.number_of_clients} clients')

    def send(self):
        pass

    def receive(self, client) -> str:
        data = b''
        while b'\r\n\r\n' not in data:
            data += client.recv(120)
        data = data.decode('utf-8')
        return data

    def receive_request(self, client) -> Request:
        rcv_data = self.receive(client)
        request = Request()
        request.parse_request(rcv_data)
        return request

class Server(ServerBase):
    def __init__(self) -> None:
        super().__init__()
        self.clients = list()
        self.dispatcher = [
            ('DRAW', self.send_draw),
            ('SEND_MESSAGE', self.send_message)
        ]
        
    def run(self):
        while True:
            client, addr = self.socket.accept()

            request = self.receive_request(client)
            if self.check_request(request):
                self.clients.append(client)

            logging.info(request.headers)

    
    def check_request(self, request):
        print(request.headers.get('Action'))
        if 'HELLO' in request.headers.get('Action'):
            return True
        else:
            return False
            
    
    def update_chat(self, client, request):
        print(request.headers.get('data'))
        client.send()
    
    def send_draw(self, request):
        pass

    def send_message(self, request):
        return


def main():
    server = Server()
    server.run()
    
    # for client in server.clients:
    #     print(client)


if __name__ == '__main__':
    main()
