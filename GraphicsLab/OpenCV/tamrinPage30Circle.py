import cv2
import numpy as np

img = cv2.imread(r'C:\Users\NoteBook\Pictures\eye.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


blurred = cv2.GaussianBlur(gray, (9, 9), 2)

circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=100,
    param1=100,
    param2=30,
    minRadius=30,
    maxRadius=70
)

if circles is not None:
    circles = np.uint16(np.around(circles))
   
    i = circles[0][0]
    cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 4)
    cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('Iris Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()