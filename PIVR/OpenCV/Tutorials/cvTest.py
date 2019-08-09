import numpy as np
import cv2
from matplotlib import pyplot as plt


def nothing(x):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow('controls')

# create trackbars for min colors
cv2.createTrackbar('minH', 'controls', 0, 255, nothing)
cv2.createTrackbar('minS', 'controls', 0, 255, nothing)
cv2.createTrackbar('minV', 'controls', 0, 255, nothing)

# create trackbars for max colors
cv2.createTrackbar('maxH', 'controls', 0, 255, nothing)
cv2.createTrackbar('maxS', 'controls', 0, 255, nothing)
cv2.createTrackbar('maxV', 'controls', 0, 255, nothing)

cv2.setTrackbarPos('maxH', 'controls', 255)
cv2.setTrackbarPos('maxS', 'controls', 255)
cv2.setTrackbarPos('maxV', 'controls', 255)

c = np.uint8([[[114,128,250]]])
hsv_c = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
print(hsv_c)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # get current positions of four trackbars
    minH = cv2.getTrackbarPos('minH', 'controls')
    minS = cv2.getTrackbarPos('minS', 'controls')
    minV = cv2.getTrackbarPos('minV', 'controls')

    maxH = cv2.getTrackbarPos('maxH', 'controls')
    maxS = cv2.getTrackbarPos('maxS', 'controls')
    maxV = cv2.getTrackbarPos('maxV', 'controls')

    # Our operations on the frame come here
    # img = frame # cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width = hsv.shape[:2]

    lower_red = np.array([minH, minS, minV])
    upper_red = np.array([maxH, maxS, maxV])

    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask_red # cv2.bitwise_or(mask_red, mask_green)

    # img = cv2.rectangle(img,(350,200),(400,250),(0,255,0),3)
    # print(img[375, 225])
    # img[350:400, 225:275] = [255, 255, 255]
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# img = cv2.imread('astronaut.png',0)
#
# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.show()