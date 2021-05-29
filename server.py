import socket
import logging
import typing as tp
from queue import Queue
from threading import Thread

from utils import receive_request
from custom_request import Request


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


HOST = 'localhost'
PORT = 1781
NUMBER_OF_CLIENTS = 2


class Game:
    def __init__(self):
        self.dispatcher = [
            ('DRAW', self.send_draw),
            ('SEND_MESSAGE', self.send_message)
        ]

    def send_draw(self, request):
        return

    def send_message(self, request):
        return

    def dispatch(self, request: Request) -> tp.List[Request]:
        return []


class Server:
    def __init__(self) -> None:
        logging.info('Creating socket')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))

        logging.info(f'Listening to {NUMBER_OF_CLIENTS} clients')
        self.socket.listen(NUMBER_OF_CLIENTS)

        self.clients = list()
        self.threads = list()

        self.queue_client = Queue()
        self.queue_sender = Queue()

    def worker(self, client):
        while True:
            # tmp = read(client, sepp='\r\n\r\n')
            request = receive_request(client)
            logging.info(f'Worker: got {request}')
            logging.info('Worker: Pushing to queueClient')
            self.queue_client.put((client, request))

    def sender_worker(self):
        while True:
            client, message = self.queue_sender.get()
            logging.info(f'Will send {message} to client')
            client.sendall(message.encode('utf-8'))
            self.queue_sender.task_done()

    def game_worker(self):
        game = Game()
        while True:
            client, request = self.queue_client.get()
            print(request)

            request: Request = request
            requests_to_send: tp.List[Request] = game.dispatch(request)

            # TODO - send requests

            for c in self.clients:
                self.queue_sender.put((c, str(request.headers)))

            self.queue_client.task_done()

    def run_worker(self, target, **kwargs):
        thread = Thread(target=target, **kwargs)
        thread.daemon = True
        thread.start()
        self.threads.append(thread)

    def run(self):
        self.run_worker(self.game_worker)
        self.run_worker(self.sender_worker)

        while True:
            logging.info('Socket accept')
            client, addr = self.socket.accept()
            self.clients.append(client)

            logging.info('Starting client worker thread')
            self.run_worker(self.worker, args=(client,))
            request = self.receive_request(client)
            if self.check_request(request):
                self.clients.append(client)

            logging.info(request.headers)

    
    def check_request(self, request):
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


if __name__ == '__main__':
    main()


# def check_request(self, request):
#     print(request.headers.get('Action'))
#     if 'HELLO' in request.headers.get('Action'):
#         return True
#     else:
#         return False
#
# def update_chat(self, client, request):
#     print(request.headers.get('data'))
#     client.send()
