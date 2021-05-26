
# --- METHODS FROM CLIENT

# LOGIN (nickname) [wpuszczamy po wpisaniu na poczatku / czy nick zajety]
# START [każdy może kliknac start]
# DRAW [tylko ten co moze rysowac]
# SEND_CHAT [wszyscy]
# [jesli rysuje-mam zabklowoany wysylanie w chat]


# --- METHODS FROM SERVER

# TURN (id)
# SEND_DRAW
# UPDATE_CHAT
# UPDATE_PLAYERS [wysylamy tez punkty] [sortujemy po ilosci punktow]
# UPDATE_REMAINING_TIME [np. 00:45]
# START_GAME
# - send to guessing string word slots np. ___ ___ __
# - send to drawer word np. ala ma kota
# SEND_END_GAME_STATUS [np. WON, LOST, 50pnkt]

#UPDATE_PLAYERS
# Action: UPDATE_PLAYERS \r\n
# Data: "{"player_list": [{"maciej": 90}, {"malika": 100}]}"

import socket
import json

host = "103.0.0.2"
port = 1780

class ServerBase:

    def __init__(self) -> None:
        self.buffer = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.client, self.addr = self.s.accept() 

    def send(self):
        pass

    def receive(self):
        """
        Action: DRAW\r\n
        Headers-Length: 2\r\n
        Content-Length: 43\r\n
        Data: 1.0, 2.2\r\n\r\n
        """
        data = b''
        while b'\r\n\r\n' not in data:
            data += self.s.recv(120)
        data = data.decode('utf-8')    

        rcv_action = data.split('\r\n')[0]
        rcv_headers_length = data.split('\r\n')[1]
        rcv_content_length = data.split('\r\n')[2]
        rcv_data = data.split('\r\n')[3]
        
        return rcv_action, rcv_content_length, rcv_data

    def parse_request(self):
        action, content_length, data = self.receive(self)
        request_obj = { 
            "action": action,
            "content_length": content_length,
            "data": data,    
        }
        return json.dumps(request_obj)

    def run(self):
        print('Server running')
        pass


class Server(ServerBase):
    def __init__(self) -> None:
        super().__init__()

        self.dispatcher = [
            ('DRAW', self.send_draw),
            ('UPDATE_CHAT', self.update_chat),
            ('SEND_CHAT', self.send_chat)
        ]

    def receive_request(self):
        # data = self.base.parse_request()
        # print(data)
        pass

    def send_draw(self, request):
        pass

    def update_chat(self):
        pass

    def send_chat(self):
        # self.base.s.sendall("tablica obiektow typu ChatMessage".encode('utf-8'))
        return


def main():
    server_base = ServerBase()
    server = Server(server_base)
    server.run()
    server.receive_request()


if __name__ == '__main__':
    main()
