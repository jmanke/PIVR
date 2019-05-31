import cv2
import numpy as np

# Contours in OpenCV - moments

# track red

cap = cv2.VideoCapture(0)
tail_buf_iter = 0
tail_buff = []
tail_buf_size = 50


def draw_trail(img):
    coords = []

    for pos in np.roll(tail_buff, tail_buf_size - tail_buf_iter, 0):
        if pos is not None:
            coords.append(pos)

    for i in range(len(coords) - 1):
        cv2.line(img, (coords[i][0], coords[i][1]), (coords[i+1][0], coords[i+1][1]), (0, 0, 255), 2)


def get_mask(img, lower, upper):
    mask = cv2.inRange(img, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    return mask


def filter_frame(frame):
    blur = cv2.GaussianBlur(frame, (11, 11), 0)
    img_output = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    return img_output


for i in range(tail_buf_size):
    tail_buff.append(None)

print(cv2.__version__)

while True:
    ret, frame = cap.read()
    filtered_img = filter_frame(frame)

    lower = (29, 86, 6)
    upper = (64, 255, 255)

    # masking colors
    green_mask = get_mask(filtered_img, lower, upper)
    res = cv2.bitwise_and(filtered_img, filtered_img, mask=green_mask)

    # find contours
    contours, hierarchy = cv2.findContours(green_mask, 1, 2)
    min_area = 200

    if len(contours) > 0:
        largest_cnt = contours[0]
        largest_area = cv2.contourArea(contours[0])
        index = 0
        ind = 0

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                continue
            elif area > largest_area:
                largest_cnt = cnt
                largest_area = area
                index = ind
            ind += 1

        if largest_area >= min_area:
            rect = cv2.minAreaRect(largest_cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            frame = cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

            # Calculate center
            M = cv2.moments(largest_cnt)

            # draw contours
            cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                tail_buff[tail_buf_iter] = (cX, cY)
            else:
                tail_buff[tail_buf_iter] = None
    else:
        tail_buff[tail_buf_iter] = None

    tail_buf_iter += 1
    tail_buf_iter %= tail_buf_size
    draw_trail(frame)

    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    res = np.hstack((frame, res))  # stacking images side-by-side
    cv2.imshow('frame', res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
exit(0)
