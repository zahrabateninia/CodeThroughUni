import cv2
import numpy as np


w, h = 600, 600
img = np.full((h, w, 3), 255, np.uint8)


def to_px(x, y):
    return (
        int((x + 1.2) * (w / 2.4)),  
        int((1.2 - y) * (h / 2.4))    
    )


for i in np.linspace(-1, 1, 9):
    cv2.line(img, to_px(i, -1.2), to_px(i, 1.2), (230, 230, 230), 1)
    cv2.line(img, to_px(-1.2, i), to_px(1.2, i), (230, 230, 230), 1)

# رسم محورهای مختصات
cv2.line(img, to_px(-1.2, 0), to_px(1.2, 0), (0, 0, 0), 2)  
cv2.line(img, to_px(0, -1.2), to_px(0, 1.2), (0, 0, 0), 2)  
cv2.circle(img, to_px(0, 0), 4, (0, 0, 0), -1)               


points = np.array([
    [-1,  1],
    [ 1,  1.15],
    [ 1,  0],
    [ 0, -1],
    [-1,  1]
], np.float32)


pts = np.array([to_px(x, y) for x, y in points], np.int32).reshape(-1, 1, 2)


cv2.polylines(img, [pts], isClosed=True, color=(255, 0, 0), thickness=2)


for i in range(len(points) - 1):
    for t in np.linspace(0, 1, 10):
        x = points[i][0] + t * (points[i + 1][0] - points[i][0])
        y = points[i][1] + t * (points[i + 1][1] - points[i][1])
        cv2.circle(img, to_px(x, y), 4, (0, 0, 255), -1)

cv2.imshow("Polygon Shape", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
