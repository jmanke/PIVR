import cv2
import numpy as np

def CornerDetection():
    img = cv2.imread('sudokuTest.png', 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
    corners = np.int0(corners)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

    cv2.imshow('dst', img)

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit(0)
            break

CornerDetection()