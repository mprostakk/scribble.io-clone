from custom_request import Request

class Client:
    def __init__(self, client, username):
        self.client = client
        self.username = username
        self.points = 0
        
    def update_score(self, points):
        self.points += points
        

def read(client, sepp='\r\n'):
    buffer = client.recv(1).decode('utf-8')

    while not (sepp in buffer):
        data = client.recv(1).decode('utf-8')
        buffer += data

    return buffer[:len(buffer)-2]


def receive(client) -> str:
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
