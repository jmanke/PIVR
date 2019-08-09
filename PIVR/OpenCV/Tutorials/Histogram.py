import cv2
import numpy as np
from matplotlib import pyplot as plt

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     # bin = 256
#     hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
#
#     cv2.imshow('frame', hsv)
#
#     plt.imshow(hist, interpolation='nearest')
#     plt.show()

    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    # cl1 = clahe.apply(graySrc)

    #hist = cv2.calcHist([cl1], [0], None, [bin], [0, bin])

    # 1D matlib plot
    # col = (0, 0, 0)
    # plt.plot(hist, color=col)
    # plt.xlim([0, bin])
    # plt.draw()
    # plt.pause(0.0001)
    # plt.clf()

    # equ = cv2.equalizeHist(cl1)
    # res = np.hstack((graySrc, cl1))

    # cv2.imshow('frame', cl1)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     print('exit')
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     exit(0)
