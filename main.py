import cv2
import numpy as np

def remove_background(image_path):
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use adaptive thresholding to create a binary image
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a mask with white pixels
    mask = np.ones_like(gray) * 255
    
    # Draw contours on the mask
    cv2.drawContours(mask, contours, -1, 0, thickness=cv2.FILLED)
    
    # Invert the mask
    mask = cv2.bitwise_not(mask)
    
    # Remove the background using bitwise_and
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result

# Path to your image
image_path = "cv.png"

# Remove background
result = remove_background(image_path)

# Display the result
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
