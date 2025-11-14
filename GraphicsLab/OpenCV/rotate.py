import cv2
img = cv2.imread('C:\Users\Asus\CodeThroughUni\GraphicsLab\OpenCV\test_image.png')
(h, w) =  img.shape[:2]
scale = 1.0
center = (w/2, h/2)
M = cv2.getRotationMatrix2D(center, 45, scale)
print(M)
rotated45 = cv2.warpAffine(img, M, (w, h))
M = cv2.getRotationMatrix2D(center, 110, scale)
rotated110 = cv2.warpAffine(img, 110, scale)

M = cv2.getRotationMatrix2D(center, 150, scale)
rotated110 = cv2.warpAffine(img, 150, scale)

cv2.imshow('original', img)
cv.imshow('image rotated by 45', rotated45)