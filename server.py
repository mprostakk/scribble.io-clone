import socket
import logging
import typing as tp
from queue import Queue
from threading import Thread
import ssl

from utils import receive_request, CustomClients
from custom_request import Request
from game_logic import Game


logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

HOST = 'localhost'
PORT = 1782
NUMBER_OF_CLIENTS = 2

class Server:
    def __init__(self) -> None:
        logging.info('Creating socket')
        self.ssl_socket = self.create_ssl_socket()
        
        self.threads = list()
        self.clients = CustomClients()

        self.queue_client: Queue = Queue()
        self.queue_sender: Queue = Queue()

    def create_ssl_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORT))
        sock.listen(NUMBER_OF_CLIENTS)

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile='certs/client.crt')
        context.load_cert_chain(certfile='certs/server.crt', keyfile='certs/server.key')
        ssl_socket = context.wrap_socket(sock, server_side=True)

        return ssl_socket

    def worker(self, client):
        while True:
            try:
                request = receive_request(client)
                request.user = self.clients.client_to_username(client)
                logging.info(f'Worker: got {request}')
                logging.info('Worker: Pushing to queueClient')
                self.queue_client.put((client, request))
            except Exception as e:
                print(str(e))
                self.clients.remove_client(client)
                break
            
    def sender_worker(self):
        while True:
            client, message = self.queue_sender.get()
            logging.info(f'Will send {message} to client')
            client.sendall(message.encode('utf-8'))
            self.queue_sender.task_done()

    def game_worker(self):
        game = Game(self.clients)
        while True:
            client, request = self.queue_client.get()

            request: Request = request
            requests_to_send: tp.List[Request] = game.dispatch(request)
            self.queue_client.task_done()

            if len(requests_to_send) == 0:
                continue

            # response from game to client
            for request_to_send in requests_to_send:
                for client_to_send in self.clients.get_clients_from_request(request_to_send):
                    data_to_send = request_to_send.parse_headers()
                    self.queue_sender.put((client_to_send, data_to_send))

    def run_worker(self, target, **kwargs):
        thread = Thread(target=target, **kwargs)
        thread.daemon = True
        thread.start()
        self.threads.append(thread)

    def run(self):
        self.run_worker(self.game_worker)
        self.run_worker(self.sender_worker)

        k = 1
        while True:
            logging.info('Socket accept')
            client, addr = self.ssl_socket.accept()

            username = f'Player {k}'
            self.clients.add_client(client, username)
            k += 1

            r = Request()
            
            r.headers['Action'] = 'INIT_PLAYER'
            r.user = username
            r.session_id = self.clients.get_session_id(username)

            self.queue_client.put((client, r))

            logging.info('Starting client worker thread')
            self.run_worker(self.worker, args=(client,))


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
