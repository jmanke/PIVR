import cv2
import numpy as np


def getNumbers():
    # start is 4x102
    # Read numbers 81x100
    img_numbers = cv2.imread('numbers.jpg')
    img_numbers = cv2.cvtColor(img_numbers, cv2.COLOR_BGR2GRAY)
    numbers = []
    # width, height of each number
    x, y = 79, 100
    # top left pixel of first number
    topleft = (4, 102)
    for i in range(2):
        topleft = (4, topleft[1] + i * y)
        for j in range(5):
            tl = (topleft[0] + j * x, topleft[1])
            br = (tl[0] + x, tl[1] + y)
            # cv2.rectangle(img_numbers, tl, br, (0, 255, 0))
            numbers.append(img_numbers[tl[1]:br[1], tl[0]:br[0]])
    # cv2.imshow('sudoku', img_numbers)
    return numbers


img_sudoku = cv2.imread('sudokuTestNoLines.png')
sudoku_gray = cv2.cvtColor(img_sudoku, cv2.COLOR_BGR2GRAY)

numbers = getNumbers()
template = numbers[1] # cv2.imread('one.png') # numbers[1]
# template = cv2.cvtColor(template, cv2.cv2.COLOR_BGR2GRAY)
w, h = template.shape[::-1]

res = cv2.matchTemplate(sudoku_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.44
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_sudoku, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

# res = cv2.matchTemplate(sudoku_gray, template, cv2.TM_CCOEFF_NORMED)
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)
#
# cv2.rectangle(img_sudoku,top_left, bottom_right, 255, 2)

cv2.imshow('sudoku', img_sudoku)
cv2.imshow('res', res)


while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('exit')
        cv2.destroyAllWindows()
        exit(0)