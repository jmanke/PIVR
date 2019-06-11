import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
from glob import glob
import time
import pipe_client

MIN_MATCH_COUNT = 5
KNOWN_DISTANCE = 85.0

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

sift = cv2.xfeatures2d.SIFT_create()


def get_cv2_img(img):
    if img:
        f = open("./image_test.jpg", "w+b")
        f.write(img)
        f.close()
        print("Image written")

    return cv2.imread("./image_test.jpg", 0)


def get_matches(train_img, target_img):
    kp1, des1 = sift.detectAndCompute(train_img, None)
    kp2, des2 = sift.detectAndCompute(target_img, None)

    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    # store all the good matches as per Lowe's ratio test.
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        matched_points = []

        # get a set of good matches
        for i in range(len(matchesMask)):
            if matchesMask[i] == 1:
                x1 = src_pts[i][0][0]
                y1 = src_pts[i][0][1]
                x2 = dst_pts[i][0][0]
                y2 = dst_pts[i][0][1]
                matched_points.append(((x1, y1), (x2, y2)))

        return matched_points

def main():
    start_time = time.time()
    handle = pipe_client.get_handle()
    train_img = get_cv2_img(pipe_client.get_train_img(handle))
    target_img = cv2.imread('./rasp_84cm.jpg', 0)

    matched_points = get_matches(train_img, target_img)

    best_fit = pipe_client.get_best_fit_img(handle, matched_points)
    get_cv2_img(best_fit)

    # h, w = train_img.shape[:2]
    # pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    # dst = cv2.perspectiveTransform(pts, M)
    #
    # target_img = cv2.polylines(target_img, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
    # print('Total = ', len(kp2), ', Found = ', len(matched_points))
    #
    # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
    #                    singlePointColor=(0, 0, 255),
    #                    matchesMask=matchesMask,  # draw only inliers
    #                    flags=2)
    #
    # img3 = cv2.drawMatches(train_img, kp1, target_img, kp2, good, None, **draw_params)
    # plt.imshow(img3, 'gray'), plt.show()
    print(time.time() - start_time)

if __name__ == "__main__":
    main()