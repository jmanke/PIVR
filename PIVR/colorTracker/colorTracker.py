import cv2
import numpy as np

# Contours in OpenCV - moments

# track red

cap = cv2.VideoCapture(0)


def get_mask(img, lower, upper):
    lower = np.array([lower])
    upper = np.array([upper])
    return cv2.inRange(filtered_img, lower, upper)


def filter_frame(frame):
    blur = cv2.bilateralFilter(frame, 12, 75, 75)
    img_yuv = cv2.cvtColor(blur, cv2.COLOR_BGR2YUV)
    # img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    # img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(5, 5))
    img_yuv[:, :, 0] = clahe.apply(img_yuv[:, :, 0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    img_output = cv2.cvtColor(img_output, cv2.COLOR_BGR2HSV)

    return img_output


while True:
    ret, frame = cap.read()
    filtered_img = filter_frame(frame)

    low_red = (100, 100, 0)
    up_red = (200, 255, 255)

    # masking colors
    red_mask = get_mask(filtered_img, (25, 150, 50), (255, 255, 255))
    res = cv2.bitwise_and(filtered_img, filtered_img, mask=red_mask)

    # find contours
    contours, hierarchy = cv2.findContours(red_mask, 1, 2)
    min_area = 100

    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        frame = cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    res = np.hstack((frame, res))  # stacking images side-by-side
    cv2.imshow('frame', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
exit(0)
