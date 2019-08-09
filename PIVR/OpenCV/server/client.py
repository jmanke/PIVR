import socket
import time
import cv2
import select
import numpy as np
import io

CLIENT_TYPE = 1


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


s = socket.socket()
host = "localhost"
port = 7777
s.connect((host, port))
s.setblocking(False)

s.send(int_to_bytes(1))

time.sleep(1)
s.send(int_to_bytes(34))

# file = open("image.jpg", "rb")
# imgData = file.read()

# s.send(imgData)

print("Waiting for data...")
c = 0

while True:
    print(c)
    c+=1
    try:
        r, _, _ = select.select([s], [], [])

        if not r:
            continue

        data = s.recv(100000)

        if data:
            # img = data

            # while data:
            #     img += data
            #     data = s.recv(100000)

            print("Size of img: ", len(data))
            # todo: convert bytes directly to img data
            filename = "./client_img.jpg"
            f = open(filename, "w+b")
            f.write(data)
            f.close()

            client_img = cv2.imread(filename, 0)
            print("All data received: ", len(client_img))
            cv2.imshow('img', client_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            

    except KeyboardInterrupt:
        s.close()
        exit(0)
