import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
from glob import glob
import time

MIN_MATCH_COUNT = 5
KNOWN_DISTANCE = 85.0
IMAGE_DUMP = "../UnityPIVR/ImageDump/*.jpg"


def get_kp_mask(matches, kp1, kp2):
    good = []

    for m, n in matches:
        if m.distance < 0.9 * n.distance:
            good.append(m)

    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        return matchesMask


def similarity(img1, img2, min_matches):
    best_dist = 10000000.0
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    good = []
    # store all the good matches as per Lowe's ratio test.
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > min_matches:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        # average distance between matches in the images
        avg_dist = 0.0
        good_matches = 0

        # print(src_pts[2][0])

        for i in range(len(matchesMask)):
            if matchesMask[i] == 1:
                x1 = src_pts[i][0][0]
                y1 = src_pts[i][0][1]
                x2 = dst_pts[i][0][0]
                y2 = dst_pts[i][0][1]
                avg_dist += math.hypot(x2 - x1, y2 - y1)
                good_matches += 1
                # cv2.circle(img1, (x1, y1), 10, (255, 255, 255), -1)
                # cv2.circle(img2, (y2, y2), 10, (255, 255, 255), -1)

        if good_matches > 0:
            avg_dist /= good_matches

        if avg_dist < best_dist:
            best_dist = avg_dist

        return best_dist
    return -1



def main():
    start_time = time.time()
    best_match_img = None
    best_match_kp = None
    best_good = None
    best_matches_mask = None
    best_dist = 10000000.0
    best_name = ""

    img2 = cv2.imread('rasp_84cm.jpg', 0)  # trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    c = 0

    for img_path in glob(IMAGE_DUMP):
        c += 1

        img1 = cv2.imread(img_path, 0)  # queryImage

        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1, None)

        matches = flann.knnMatch(des1, des2, k=2)

        good = []
        # store all the good matches as per Lowe's ratio test.
        for m, n in matches:
            if m.distance < 0.6 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()

            # average distance between matches in the images
            avg_dist = 0.0
            good_matches = 0

            # print(src_pts[2][0])

            for i in range(len(matchesMask)):
                if matchesMask[i] == 1:
                    x1 = src_pts[i][0][0]
                    y1 = src_pts[i][0][1]
                    x2 = dst_pts[i][0][0]
                    y2 = dst_pts[i][0][1]
                    avg_dist += math.hypot(x2-x1, y2-y1)
                    good_matches += 1
                    # cv2.circle(img1, (x1, y1), 10, (255, 255, 255), -1)
                    # cv2.circle(img2, (y2, y2), 10, (255, 255, 255), -1)

            if good_matches > 0:
                avg_dist /= good_matches
            else:
                continue

            if avg_dist < best_dist:
                best_dist = avg_dist
                best_match_img = img1
                best_match_kp = kp1
                best_good = good
                best_name = img_path
                best_matches_mask = matchesMask

            print(c, ': ', img_path, ' = ', avg_dist, ', current best = ', best_dist)
            # good_len = len(good)
            # good_copy = good.copy()
            #
            # for i in range(good_len):
            #     index = good_len - i - 1
            #     if matchesMask[index] == 0:
            #         del good_copy[index]
            #

            # h, w = img1.shape[:2]
            # pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            # dst = cv2.perspectiveTransform(pts, M)
            #
            # img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)
            # print('Total = ', len(kp2), ', Found = ', len(matchesMask))
            #
            # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
            #                    singlePointColor=(0, 0, 255),
            #                    matchesMask=matchesMask,  # draw only inliers
            #                    flags=2)
            #
            # img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
            # plt.imshow(img3, 'gray'), plt.show()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            continue

        else:
            print
            "Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT)
            matchesMask = None

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=(0, 0, 255),
                       matchesMask=best_matches_mask,  # draw only inliers
                       flags=2)

    print(best_name, ': ', best_dist)
    print('running time = ', time.time() - start_time)
    img3 = cv2.drawMatches(best_match_img, best_match_kp, img2, kp2, best_good, None, **draw_params)
    plt.imshow(img3, 'gray'), plt.show()

main()
print("Done")
