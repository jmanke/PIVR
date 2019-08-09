import numpy as np
import cv2

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

cv2.namedWindow('controls', cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar('a', 'controls', 0, 255, nothing)
cv2.createTrackbar('b', 'controls', 0, 255, nothing)
cv2.createTrackbar('c', 'controls', 0, 25, nothing)

cv2.setTrackbarPos('a', 'controls', 100)
cv2.setTrackbarPos('b', 'controls', 200)
cv2.setTrackbarPos('c', 'controls', 3)

while True:
    ret, frame = cap.read()

    a = cv2.getTrackbarPos('a', 'controls')
    b = cv2.getTrackbarPos('b', 'controls')
    c = cv2.getTrackbarPos('c', 'controls')

    if a % 2 == 0:
        cv2.setTrackbarPos('a', 'controls', a + 1)
        a += 1

    srcGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(srcGray,9,10,75)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, a, b)
    edges = cv2.Canny(blur, a, b, 3)
    # ret1, thresh = cv2.threshold(srcGray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(len(contours))
    img = cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)

    cv2.namedWindow('dst', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('dst', edges)

    # blur = cv2.blur(srcGray, (b, b), 0)
    # dst = cv2.Sobel(srcGray, cv2.CV_16S, 1, 1, ksize=a)
    # absDst = np.absolute(dst)
    # dst_8u = np.uint8(absDst)
    # img = cv2.bilateralFilter(img, a, b, c)
    # img = cv2.resize(img, None, fx=a, fy=b, interpolation=cv2.INTER_CUBIC)
    # rows, cols = img.shape
    # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), a, 1)
    # M = np.float32([[1, 0, a], [0, 1, b]])
    # dst = cv2.warpAffine(img, M, (cols, rows))

    # if b % 2 != 1:
    #     cv2.setTrackbarPos('blockSize', 'controls', b + 1)
    #     b += 1
    #
    # if b <= 1:
    #     cv2.setTrackbarPos('blockSize', 'controls', 3)
    #     blockSize = 3

    # blur = cv2.GaussianBlur(img, (5, 5), 0)
    # ret1, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # th1 = cv2.adaptiveThreshold(th,255,cv2.ADAPTIVE_THRESH_MEAN_C,
    #          cv2.THRESH_BINARY,5,ret1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()