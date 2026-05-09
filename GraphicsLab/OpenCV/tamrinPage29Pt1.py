import cv2
import numpy as np

image = cv2.imread('test_image.png')

if image is None:
    print("Error: image not found")
    exit()


cv2.imshow('Original Image', image)
gray_manual = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

for i in range(image.shape[0]): 
    for j in range(image.shape[1]):  
        b, g, r = image[i, j]
        gray_value = (int(b) + int(g) + int(r)) // 3
        gray_manual[i, j] = gray_value

cv2.imshow('Manual Grayscale', gray_manual)
cv2.imwrite('test_image.png', gray_manual)

height = 360
width = 640
ellipse_image = np.zeros((height, width, 3), dtype=np.uint8)

center = (width // 2, height // 2)
axes = (150, 80)  
color = (255, 255, 255)  # white 
thickness = 2

for angle in range(0, 360):
    temp_image = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.ellipse(temp_image, center, axes, angle, 0, 360, color, thickness)
    cv2.putText(temp_image, f'Angle: {angle}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Ellipse Rotation', temp_image)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.ellipse(ellipse_image, center, axes, 45, 0, 360, color, thickness)
cv2.imwrite('exercise2_ellipse.jpg', ellipse_image)


circle_image_height = 600
circle_image_width = 600
circle_center = (circle_image_width // 2, circle_image_height // 2)

for radius in range(0, 501, 5):
    temp_image = np.zeros((circle_image_height, circle_image_width, 3), dtype=np.uint8)
    cv2.circle(temp_image, circle_center, radius, (0, 255, 0), 2)
    cv2.putText(temp_image, f'Radius: {radius}', (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Circle Radius', temp_image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

circle_final = np.zeros((circle_image_height, circle_image_width, 3), dtype=np.uint8)
cv2.circle(circle_final, circle_center, 250, (0, 255, 0), 2)
cv2.imwrite('exercise3_circle.jpg', circle_final)


cv2.waitKey(0)
cv2.destroyAllWindows()
