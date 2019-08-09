import cv2
import numpy as np

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

template = cv2.imread('soccer_ball.png', 0)
src = cv2.imread('soccer_full.png', 0)

w, h = template.shape[::-1]

# Apply template Matching
res = cv2.matchTemplate(src, template, cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(src,top_left, bottom_right, 255, 2)

cv2.imshow('match', src)

print(w, ", ", h)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('exit')
        cv2.destroyAllWindows()
        exit(0)