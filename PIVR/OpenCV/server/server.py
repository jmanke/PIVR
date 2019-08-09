#!/usr/bin/python

import socket
import select
import os
import io
import os.path

python_client = None
unity_client = None


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')


def handle_python_data(data):
    if data:
        pass


def handle_unity_data(data):
    # unity client only sends images
    if data:
        f = open("./image_server.jpg", "w+b")
        # img = data
        # data = unity_client.recv(100000)

        # while data:
        #     img += data
        #     python_client.send(data)
        #     data = unity_client.recv(100000)

        print("Size of img: ", len(data))
        f.write(data)
        python_client.send(data)


def main():
    s = socket.socket()
    host = "localhost"
    print(host)
    port = 7777
    s.bind((host, port))
    global python_client
    global unity_client

    while python_client is None or unity_client is None:
        s.listen(1)
        print("Waiting for a connection...")
        c, addr = s.accept()
        data = c.recv(1024)
        c_type = int_from_bytes(data)
        if c_type == 1:
            python_client = c
        elif c_type == 2:
            unity_client = c

    print("Press 'ctrl' + 'c' to stop server...")

    c = 0
    while True:
        print(c)
        c+=1
        try:
            r_p, _, _ = select.select([python_client], [], [])
            r_c, _, _ = select.select([unity_client], [], [])
            if r_p:
                handle_python_data(python_client.recv(100000))
            if r_c:
                handle_unity_data(unity_client.recv(100000))
        except KeyboardInterrupt:
            unity_client.close()
            python_client.close()
            s.close()
            print("Done.")
            exit(0)
        else:
            print("hanging")

if __name__ == "__main__":
    main()