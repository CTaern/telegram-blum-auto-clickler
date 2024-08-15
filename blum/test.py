import cv2
import numpy as np

# Use the correct file path for your local machine
image_path = "C:/Users/Taner/Desktop/Screenshot 2024-08-09 160300.png"
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    print("Error: Image not found or cannot be opened.")
else:
    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Manually set a region of interest (ROI) around the bomb to detect its color range
    roi = hsv_image[0:15, 0:15]  # You may need to adjust these coordinates

    # Calculate the mean and standard deviation of the ROI to get the color range
    mean_hsv = np.mean(roi, axis=(0, 1))
    std_hsv = np.std(roi, axis=(0, 1))

    # Define the lower and upper bounds for the bomb color in HSV
    lower_bomb = np.clip(mean_hsv - std_hsv, 0, 255)
    upper_bomb = np.clip(mean_hsv + std_hsv, 0, 255)

    print("Lower HSV Bound for Bomb:", lower_bomb)
    print("Upper HSV Bound for Bomb:", upper_bomb)
