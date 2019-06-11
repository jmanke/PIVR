import time
import sys
import struct
import numpy as np
import win32pipe, win32file, pywintypes


def get_handle():
    try:
        handle = win32file.CreateFile(
            r'\\.\pipe\PIVR_pipe',
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )
        return handle
    except pywintypes.error as e:
        if e.args[0] == 2:
            print("no pipe")
        elif e.args[0] == 109:
            print("broken pipe")


def get_train_img(handle):
    if handle:
        data = "heyyy"
        data_type = (1).to_bytes(1, byteorder="little")
        encoded_data = str.encode(f"{data}")
        data_len = len(encoded_data).to_bytes(4, byteorder="little")
        msg = b''.join([data_type, data_len, encoded_data])
        win32file.WriteFile(handle, msg)
        print("Sending data...")
        print("Waiting for data...")
        resp = win32file.ReadFile(handle, 64 * 1024)
        print("Data received...")
        return resp[1]
    else:
        print("Could not get handle")


# get a best fit image from Unity
# kp = list of tuples containing keypoints from training image and real image
def get_best_fit_img(handle, kp):
    data = np.array(kp)
    data = np.ndarray.flatten(data)
    print(len(data), "  ", kp)
    data_type = (2).to_bytes(1, byteorder="little")
    encoded_data = np.ndarray.tobytes(data)
    data_len = len(encoded_data).to_bytes(4, byteorder="little")
    msg = b''.join([data_type, data_len, encoded_data])
    win32file.WriteFile(handle, msg)
    print("Sending data...")
    print("Waiting for best fit...")
    resp = win32file.ReadFile(handle, 64 * 1024)
    print("Data best fit...")
    return resp[1]