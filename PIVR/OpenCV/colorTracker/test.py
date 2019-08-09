import cv2
import numpy as np

col = np.uint8([[[0, 0, 255]]])
hsv_col = cv2.cvtColor(col, cv2.COLOR_BGR2HSV)
print(hsv_col)