import socket

host = "127.0.0.1"
port = 1780


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

send_data = 'Action: DRAW \r\nUser: maciej \r\nData: 1.0, 2.2 \r\n\r\n'
    