import cv2


img = cv2.imread(r'C:\Users\NoteBook\Pictures\eye1.jpg')

eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)


for (x, y, w, h) in eyes:
    reduced_height = int(h * 0.6)  
    y_offset = int(h * 0.2)        
    cv2.rectangle(img, (x, y + y_offset), (x + w, y + y_offset + reduced_height), (0, 0, 255), 2)


cv2.imshow("Detected Eyes", img)
cv2.imwrite("output_eye_detected_adjusted.jpg", img)

cv2.waitKey(0)
cv2.destroyAllWindows()

