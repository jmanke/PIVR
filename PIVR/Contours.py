import cv2
import numpy as np

img = cv2.imread('handByJeff.png',1)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,125,255,0)

# imgCan = cv2.Canny(thresh, 100, 150)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(img, contours, 1, (0, 255, 0), 2)
cnt = contours[1]
M = cv2.moments(cnt)

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

# centroid
img = cv2.circle(img, (cx, cy), 3, (0, 0, 255), 1)
img = cv2.putText(img, 'centroid', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
print(cx, ', ', cy)

print(len(contours))

#convex hull
# hull = [1]
# hull[0] = cv2.convexHull(contours[1])
# img = cv2.drawContours(img, hull, 0, (0, 0, 255, 1))

hull = cv2.convexHull(contours[1],returnPoints = False)
defects = cv2.convexityDefects(contours[1],hull)

for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img,start,end,[0,255,0],2)
    cv2.circle(img,far,3,[0,0,255],-1)

cv2.imshow('hand', img)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
exit(0)