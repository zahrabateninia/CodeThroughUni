
import cv2  
import numpy as np  # For numerical operations
# Load the image (PDF page 6: Images are made of pixels in RGB, each channel 0-255)
image_path = 'test_image.png'  # Replace with your test image name if different
img = cv2.imread(image_path)  # Read the image in BGR format (OpenCV default; PDF mentions RGB, but OpenCV uses BGR internally)

if img is None:  
    print("Error: Could not load image. Check the file path.")
    exit()

# Display original image (RGB-like structure)
cv2.imshow('Original Image (BGR)', img)
print("Original image shape:", img.shape)  # Shows height, width, channels (e.g., for RGB: 3 channels)

# Step 2: Convert to Grayscale (PDF page 8: Grayscale images for faster processing)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert BGR to grayscale (single channel, 0-255)
cv2.imshow('Grayscale Image', gray)
print("Grayscale image shape:", gray.shape)  # Single channel

# Improve brightness/contrast in grayscale (PDF page 3: Improving brightness and contrast)
# Simple brightness increase by adding a value to each pixel
brightness_factor = 50  # Adjust as needed (positive for brighter, negative for darker)
bright_gray = cv2.add(gray, brightness_factor)  # Increase brightness
cv2.imshow('Brightened Grayscale', bright_gray)

# Step 3: Convert to Binary (PDF page 9: Binary images using 0 and 1/255, often via thresholding)
# Apply threshold to create binary image (e.g., pixels > 127 become 255, others 0)
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # Thresholding for binary
cv2.imshow('Binary Image', binary)

# Step 4: Filtering (PDF page 3: Filtering as an example algorithm)
# Apply a simple blur filter to reduce noise
blurred = cv2.GaussianBlur(img, (5, 5), 0)  # Gaussian blur with 5x5 kernel
cv2.imshow('Filtered (Blurred) Image', blurred)

# Edge Detection 
# Use Canny edge detector on grayscale image
edges = cv2.Canny(gray, 100, 200)  # Thresholds for edge strength
cv2.imshow('Edges Detected', edges)

# Step 6: Object Detection Example (PDF page 3: Detecting specific objects; simple contour detection here)
# Find contours in binary image (basic shape detection)
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Draw contours on original image copy
img_contours = img.copy()
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)  
cv2.imshow('Image with Contours (Object Detection)', img_contours)
print("Number of detected contours (objects):", len(contours))


cv2.waitKey(0)
cv2.destroyAllWindows()


cv2.imwrite('grayscale_output.png', gray)
cv2.imwrite('binary_output.png', binary)
cv2.imwrite('edges_output.png', edges)
print("Processed images saved.")
