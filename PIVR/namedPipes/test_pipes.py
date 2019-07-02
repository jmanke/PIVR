import numpy as np
import cv2
import math
import os
from matplotlib import pyplot as plt
from glob import glob
import time
import pipe_client
import glob

MIN_MATCH_COUNT = 5
KNOWN_DISTANCE = 85.0

FLANN_INDEX_KDTREE = 0


def get_cv2_img(img):
    if img:
        f = open("./image_test.jpg", "w+b")
        f.write(img)
        f.close()
        # print("Image written")

    return cv2.imread("./image_test.jpg", 0)


def similarity(img1, img2, min_matches):
    best_dist = 10000000.0
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    # store all the good matches as per Lowe's ratio test.
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)

    if len(good) > min_matches:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        # average distance between matches in the images
        avg_dist = 0.0
        good_matches = 0

        for i in range(len(src_pts)):
            x1 = src_pts[i][0][0]
            y1 = src_pts[i][0][1]
            x2 = dst_pts[i][0][0]
            y2 = dst_pts[i][0][1]
            dist = math.hypot(x2 - x1, y2 - y1)
            # print(f"{matchesMask[i]}: {src_pts[i]}, {dst_pts[i]}, dist = {dist}")

        for i in range(len(matchesMask)):
            if matchesMask[i] == 1:
                x1 = src_pts[i][0][0]
                y1 = src_pts[i][0][1]
                x2 = dst_pts[i][0][0]
                y2 = dst_pts[i][0][1]
                avg_dist += math.hypot(x2 - x1, y2 - y1)
                # print(f"({x1}, {y1}), ({x2}, {y2})")
                good_matches += 1
                #cv2.circle(img2, (x1, y1), 5, (255, 255, 255), -1)
                #cv2.circle(img1, (x2, y2), 5, (255, 255, 255), -1)

        h, w = img1.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
        print('Total = ', len(kp2), ', Found = ', len(matchesMask))

        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=(0, 0, 255),
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)

        img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        # plt.imshow(img3, 'gray'), plt.show()

        if good_matches > 0:
            avg_dist /= good_matches

        if avg_dist < best_dist:
            best_dist = avg_dist

        return best_dist
    return -1


def get_matches(train_img, target_img):
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(train_img, None)
    kp2, des2 = sift.detectAndCompute(target_img, None)

    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

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
        #
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

        return matched_points

def main():
    start_time = time.time()
    handle = pipe_client.handle()
    train_img = get_cv2_img(pipe_client.train_img(handle))
    image_dir = 'testImages/'

    for filename in glob.glob(os.path.join(image_dir, '*.jpg')):
        target_img = cv2.imread(filename, 0)
        matched_points = get_matches(train_img, target_img)
        if matched_points is None or len(matched_points) < 2:
            print("No matches: ", filename)
            continue
        im = pipe_client.best_fit_img(handle, matched_points)
        best_fit = get_cv2_img(im)
        avg_dist = similarity(target_img, best_fit, 5)
        print('avg_dist = ', avg_dist)
        print('len = ', len(best_fit), ', ', len(target_img))

        res = np.hstack((best_fit, train_img, target_img))
        cv2.imshow('result', res)
        print(time.time() - start_time)

        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# def main():
#     start_time = time.time()
#     handle = pipe_client.handle()
#     train_img = get_cv2_img(pipe_client.train_img(handle))
#     target_img = cv2.imread('./rasp_test.jpg', 0)
#
#     matched_points = get_matches(train_img, target_img)
#
#     best_fits = []
#
#     for i in range(1):
#         im = pipe_client.best_fit_img(handle, matched_points)
#         best_fit = get_cv2_img(im)
#         avg_dist = similarity(target_img, best_fit, 5)
#         print('avg_dist = ', avg_dist)
#         print('len = ', len(best_fit), ', ', len(target_img))
#         best_fits.append(best_fit)
#
#     res = np.hstack((best_fits[0], train_img, target_img))
#     cv2.imshow('result', res)
#     print(time.time() - start_time)
#
#     while True:
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

if __name__ == "__main__":
    main()