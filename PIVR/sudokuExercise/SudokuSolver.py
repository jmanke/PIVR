import cv2
import numpy as np

sudoku = cv2.imread('sudokuTest.png', 0)

cv2.imshow('sudoku', sudoku)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('exit')
        cv2.destroyAllWindows()
        exit(0)