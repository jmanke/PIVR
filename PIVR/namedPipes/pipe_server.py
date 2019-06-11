import time
import sys
import struct
import win32pipe, win32file, pywintypes


def pipe_server():
    print("pipe server")
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\PIVR',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    try:
        print("waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("got client")

        while count < 10:
            print(f"writing message {count}")
            # convert to bytes
            some_data = str.encode(f"{count}")
            win32file.WriteFile(pipe, some_data)
            time.sleep(1)
            resp = win32file.ReadFile(pipe, 64 * 1024)
            print(f"server: {resp}")
            count += 1

        print("finished now")
    finally:
        win32file.CloseHandle(pipe)


def pipe_client():
    print("pipe client")
    quit = False

    while not quit:
        try:
            handle = win32file.CreateFile(
                r'\\.\pipe\pipe_PIVR',
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            # res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            # if res == 0:
            #     print(f"SetNamedPipeHandleState return code: {res}")
            while True:
                data = "heyyy"
                encoded_data = str.encode(f"{data}")
                data_len = len(encoded_data).to_bytes(4, byteorder="little")
                msg =  b''.join([data_len, encoded_data])
                win32file.WriteFile(handle, msg)
                print("Sending data...")
                time.sleep(1)
                # resp = win32file.ReadFile(handle, 64*1024)
                # print(resp[1])
                # f = open("./image_test.jpg", "w+b")
                # f.write(resp[1])
                # print(f"message: {resp}")
        except pywintypes.error as e:
            if e.args[0] == 2:
                print("no pipe, trying again in a sec")
                time.sleep(1)
            elif e.args[0] == 109:
                print("broken pipe, bye bye")
                quit = True


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("need s or c as argument")
    # elif sys.argv[1] == "s":
    #     pipe_server()
    # elif sys.argv[1] == "c":
        pipe_client()
    # else:
    #     print(f"no can do: {sys.argv[1]}")