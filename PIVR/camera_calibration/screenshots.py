import cv2
import time

DELAY = 1
NUM_SCREENSHOTS = 50

cap = cv2.VideoCapture(0)
time.sleep(3)

for i in range(NUM_SCREENSHOTS):
    time.sleep(DELAY)
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    path = 'C:/Users/jeffm/Documents/github/PIVR/PIVR/camera_calibration/data/left_' + str(i) + '.jpg'
    cv2.imwrite(path, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
exit(0)