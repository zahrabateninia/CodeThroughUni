import cv2
import numpy as np


img1 = np.ones((500, 500, 3), dtype=np.uint8) * 255

cv2.line(img1, (150, 100), (250, 200), (255, 0, 0), 3)
cv2.line(img1, (250, 200), (350, 100), (255, 0, 0), 3)
cv2.line(img1, (150, 400), (250, 300), (255, 0, 0), 3)
cv2.line(img1, (250, 300), (350, 400), (255, 0, 0), 3)
cv2.line(img1, (150, 100), (150, 400), (255, 0, 0), 3)
cv2.line(img1, (350, 100), (350, 400), (255, 0, 0), 3)


cv2.putText(img1, 'Polygon Edges', (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 0, 0), 2, cv2.LINE_AA)


img2 = np.ones((500, 500, 3), dtype=np.uint8) * 255

points = np.array([
    [150, 100],
    [250, 200],
    [350, 100],
    [350, 400],
    [250, 300],
    [150, 400]
], dtype=np.int32)

cv2.fillPoly(img2, [points], (255, 0, 0))


cv2.putText(img2, 'Filled Polygon', (110, 50), cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 0, 0), 2, cv2.LINE_AA)

combined = np.hstack([img1, img2])


cv2.imshow('Shape Comparison', combined)
cv2.waitKey(0)
cv2.destroyAllWindows()