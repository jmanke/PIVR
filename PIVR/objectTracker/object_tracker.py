import cv2
import sys
import numpy as np

cap = cv2.VideoCapture(0)
initBB = None
tracker = cv2.TrackerCSRT_create()


def get_mask(img, lower, upper):
    mask = cv2.inRange(img, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask


def get_contours(frame):
    srcGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(srcGray, 9, 10, 75)
    edges = cv2.Canny(blur, 100, 200, 3)
    # ret1, thresh = cv2.threshold(srcGray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    (H, W) = frame.shape[:2]
    blank_image = np.zeros((H, W, 3), np.uint8)

    return cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 1)


lower = (30, 60, 60)
upper = (85, 255, 255)

while True:
    ret, frame = cap.read()
    key = cv2.waitKey(1) & 0xFF
    src_blur = cv2.bilateralFilter(frame, 9, 10, 75)
    # img = get_contours(frame)

    # filter frame
    src_hsv = cv2.cvtColor(src_blur, cv2.COLOR_BGR2HSV)

    # masking colors
    green_mask = get_mask(src_hsv, lower, upper)
    res = cv2.bitwise_and(src_hsv, src_hsv, mask=green_mask)
    contours, hierarchy = cv2.findContours(green_mask, 1, 2)

    if len(contours) > 0:
        largest_cnt = contours[0]
        largest_area = cv2.contourArea(contours[0])
        index = 0
        ind = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 200:
                continue
            if area > largest_area:
                largest_cnt = cnt
                largest_area = area
                index = ind
            ind += 1

        # dilate = 2
        # x, y, w, h = cv2.boundingRect(largest_cnt)
        # w_dilated = int(w * dilate)
        # h_dilated = int(h * dilate)
        # x -= int((w_dilated - w) / 2)
        # y -= int((h_dilated - h) / 2)
        # cv2.rectangle(frame, (x, y), (x + w_dilated, y + h_dilated), (0, 255, 0), 2)

        # if w_dilated > 0 and h_dilated > 0:
            # frame = frame[y:y+h_dilated, x:x+w_dilated]
            # frame = get_contours(frame)

        # Calculate center
        M = cv2.moments(largest_cnt)

        (x, y), radius = cv2.minEnclosingCircle(largest_cnt)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(frame, center, radius, (0, 255, 0), 3)

    # frame = get_contours(frame)
    cv2.imshow('frame', frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
exit(0)