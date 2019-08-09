#!/usr/bin/env python

'''
camera calibration for distorted images with chess board samples
reads distorted images, calculates the calibration and write undistorted images
usage:
    calibrate.py [--debug <output path>] [--square_size] [<image mask>]
default values:
    --debug:    ./output/
    --square_size: 1.0
    <image mask> defaults to ../data/left*.jpg
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import time

# built-in modules
import os

#from common import splitfn
def splitfn(file_path):

    file_path_parts = file_path.split(sep=os.sep)
    _path = os.path.join(*file_path_parts[:-1])
    file_name = file_path_parts[-1]
    file_name_parts = file_name.split(sep='.')
    return _path, file_name_parts[0], file_name_parts[1]

def main():
    import sys
    import getopt
    from glob import glob

    args, img_mask = getopt.getopt(sys.argv[1:], '', ['debug=', 'square_size=', 'threads='])
    args = dict(args)
    args.setdefault('--debug', './output/')
    args.setdefault('--square_size', 15)
    args.setdefault('--threads', 4)

    cap = cv.VideoCapture(0)

    # if not img_mask:
    #     img_mask = './data/left??.jpg'  # default
    # else:
    #     print(img_mask)
    #     img_mask = img_mask[0]
    #
    # img_names = glob(img_mask)

    debug_dir = args.get('--debug')

    if debug_dir and not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)

    square_size = float(args.get('--square_size'))

    pattern_size = (9, 6)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    ret, img = cap.read()
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    h, w = img.shape[:2] # cv.imread(img, cv.IMREAD_GRAYSCALE).shape[:2]  # TODO: use imquery call to retrieve results

    def processImage(img):
        # print('processing %s... ' % img)
        # img = cv.imread(fn, 0)
        if img is None:
            print("Failed to load", img)
            return None

        assert w == img.shape[1] and h == img.shape[0], ("size: %d x %d ... " % (img.shape[1], img.shape[0]))
        found, corners = cv.findChessboardCorners(img, pattern_size)
        if found:
            term = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 30, 0.1)
            cv.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        # if debug_dir:
        #     vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        #     cv.drawChessboardCorners(vis, pattern_size, corners, found)
        #     _path, name, _ext = splitfn(img)
        #     outfile = os.path.join(debug_dir, name + '_chess.png')
        #     cv.imwrite(outfile, vis)

        if not found:
            print('chessboard not found')
            return None

        print('... OK')
        return (corners.reshape(-1, 2), pattern_points)

    # threads_num = int(args.get('--threads'))
    # if threads_num <= 1:
    #     chessboards = [processImage(fn) for fn in img_names]
    # else:
    #     print("Run with %d threads..." % threads_num)
    #     from multiprocessing.dummy import Pool as ThreadPool
    #     pool = ThreadPool(threads_num)
    #     chessboards = pool.map(processImage, img_names)

    # chessboards = [x for x in chessboards if x is not None]

    chessboards = []
    good_count = 0

    while True:
        #time.sleep(1)
        ret, frame = cap.read()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        chessboard = processImage(frame)

        if chessboard is not None:
            chessboards.append(chessboard)
            good_count += 1

        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    for (corners, pattern_points) in chessboards:
        img_points.append(corners)
        obj_points.append(pattern_points)

    # calculate camera distortion
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, (w, h), None, None)

    print("\nRMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("distortion coefficients: ", dist_coefs.ravel())

    output = open("results_2.txt", "w+")
    out_rms = "\nRMS:" + str(rms)
    out_camera_matrix = "\ncamera matrix:\n" + str(camera_matrix)
    out_dist_coefs = "\ndistortion coefficients: " + str(dist_coefs.ravel())
    output.write(out_rms)
    output.write(out_camera_matrix)
    output.write(out_dist_coefs)

    # undistort the image with the calibration
    print('')
    # for fn in img_names if debug_dir else []:
    #     path, name, ext = splitfn(fn)
    #     img_found = os.path.join(debug_dir, name + '_chess.png')
    #     outfile = os.path.join(debug_dir, name + '_undistorted.png')
    #
    #     img = cv.imread(img_found)
    #     if img is None:
    #         continue
    #
    #     h, w = img.shape[:2]
    #     newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1, (w, h))
    #
    #     dst = cv.undistort(img, camera_matrix, dist_coefs, None, newcameramtx)
    #
    #     # crop and save the image
    #     x, y, w, h = roi
    #     dst = dst[y:y+h, x:x+w]
    #
    #     print('Undistorted image written to: %s' % outfile)
    #     cv.imwrite(outfile, dst)

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()