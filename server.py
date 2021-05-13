
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


# SEND_CHAT
# Action: SEND_CHAT \r\n
# User: username \r\n
# Data: string \r\n


import socket


class ServerBase:

    def __init__(self) -> None:
        self.buffer = []

    def send(self):
        pass

    def receive(self):
        """
        Action: DRAW \r\n
        User: maciej \r\n
        Data: 1.0, 2.2 \r\n
        \r\n\r\n
        """
        pass

    def parse_message():
        """
        {
            'Action': 'DRAW',
            'User': 'maciej',
            'Data': '1.0, '2.2'
        }
        """
        pass

    def run():
        pass


class Server(ServerBase):
    def __init__(self) -> None:
        super().__init__()

        self.dispatcher = [
            ('DRAW', self.send_draw),
            ('UPDATE_CHAT', self.update_chat),
            ('SEND_CHAT', self.send_chat)
        ]

    def get(self):
        data = self.receive()

    def send_draw(self, request):
        pass

    def send_chat():
        return

    def update_chat(self):
        pass


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
