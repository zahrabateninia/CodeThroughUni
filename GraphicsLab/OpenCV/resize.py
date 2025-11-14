import cv2

# Read the image
img = cv2.imread('C:\Users\Asus\CodeThroughUni\GraphicsLab\OpenCV\test_image.png')

# Check if image was loaded successfully
if img is None:
    print("Error: Could not load image. Make sure 'test_image.png' exists in the same folder.")
else:
    # Get original dimensions
    height, width = img.shape[:2]
    print(f"Original size: {width}x{height}")
    
    # METHOD 1: Resize to specific dimensions (e.g., 500x300)
    new_width = 500
    new_height = 300
    resized1 = cv2.resize(img, (new_width, new_height))
    
    scale_percent = 50  # percent of original size
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    resized2 = cv2.resize(img, (new_width, new_height))
    
    new_width = 400
    aspect_ratio = width / height
    new_height = int(new_width / aspect_ratio)
    resized3 = cv2.resize(img, (new_width, new_height))
    
    # Display images
    cv2.imshow('Original Image', img)
    cv2.imshow('Resized - Fixed Size (500x300)', resized1)
    cv2.imshow('Resized - 50% Scale', resized2)
    cv2.imshow('Resized - Preserve Aspect Ratio', resized3)
    
    print(f"Resized (fixed): {resized1.shape[1]}x{resized1.shape[0]}")
    print(f"Resized (50%): {resized2.shape[1]}x{resized2.shape[0]}")
    print(f"Resized (aspect preserved): {resized3.shape[1]}x{resized3.shape[0]}")
    
    # Wait for key press
    print("\nPress any key to save and close...")
    cv2.waitKey(0)
    
    # Save the resized images
    cv2.imwrite('resized_fixed.png', resized1)
    cv2.imwrite('resized_50percent.png', resized2)
    cv2.imwrite('resized_aspect.png', resized3)
    print("Resized images saved!")
    
    # Close all windows
    cv2.destroyAllWindows()
