import socket
import time

CLIENT_TYPE = 1


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


s = socket.socket()
host = "localhost"
port = 7777
s.connect((host, port))

s.send(int_to_bytes(1))

time.sleep(1)
s.send(int_to_bytes(34))

# file = open("image.jpg", "rb")
# imgData = file.read()

# s.send(imgData)

s.close()