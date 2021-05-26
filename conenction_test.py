import socket

host = "103.0.0.2"
port = 1780


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

send_data = 'Action: DRAW\r\nHeaders-Length: 2\r\nContent-Length: 43\r\nData: 1.0, 2.2\r\n\r\n'
    