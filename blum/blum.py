import pyautogui
import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import messagebox

# Initialize global variables to store the selected region
region = None
root = tk.Tk()

def select_area():
    global region
    messagebox.showinfo("Area Selection", "Move your cursor to the top-left corner of the area and wait...")
    time.sleep(2)
    top_left = pyautogui.position()
    
    messagebox.showinfo("Area Selection", "Now move your cursor to the bottom-right corner of the area and wait...")
    time.sleep(2)
    bottom_right = pyautogui.position()
    
    region = (top_left.x, top_left.y, bottom_right.x - top_left.x, bottom_right.y - top_left.y)
    area_label.config(text=f"Selected area: {region}")

def start_script():
    if region is None:
        messagebox.showerror("Error", "You must select an area first!")
        return
    
    duration = 30  # Define how long the script should run
    
    # Specific RGB values you want to detect for the flower
    flower_colors = [
        [214, 230, 49],  # Example RGB value 1
        [199, 247, 55], # Example RGB value 2
    ]
    
    # Specific RGB values for bomb detection
    bomb_colors = [
        [176, 176, 176],  # Example RGB value 1 for bomb
        [207, 207, 207],  # Example RGB value 2 for bomb
        [137, 129, 129],  # Example RGB value 3 for bomb
        [91, 91, 91],  # Example RGB value 4 for bomb
    ]
    
    # Tolerance for color matching
    tolerance = 30
    
    min_area = 9
    bomb_check_area = 5  # 5x5 pixels check around the flower center
    
    start_time = time.time()
    last_positions = []
    while time.time() - start_time < duration:
        screenshot = pyautogui.screenshot(region=region)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Convert the image to RGB for specific color detection
        rgb_image = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        
        # Create an empty mask to accumulate color matches for flowers
        flower_mask = np.zeros((rgb_image.shape[0], rgb_image.shape[1]), dtype=np.uint8)
        
        # Check each target flower color
        for color in flower_colors:
            lower_bound = np.array([max(0, c - tolerance) for c in color])
            upper_bound = np.array([min(255, c + tolerance) for c in color])
            
            # Create a mask for each flower color and combine them
            color_mask = cv2.inRange(rgb_image, lower_bound, upper_bound)
            flower_mask = cv2.bitwise_or(flower_mask, color_mask)
        
        # Detect contours in the flower mask
        contours, _ = cv2.findContours(flower_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        click_positions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            
            # Filter out long, thin contours (likely grid lines)
            if w * h >= min_area and (0.5 < aspect_ratio < 2.0):
                center_x = region[0] + x + w // 2
                center_y = region[1] + y + h // 2
                
                # Avoid clicking on positions near previously clicked locations
                if not any(abs(center_x - pos[0]) < 5 and abs(center_y - pos[1]) < 5 for pos in last_positions):
                    
                    # Check a 5x5 area around the flower's center for bomb colors
                    bomb_detected = False
                    small_area = rgb_image[max(0, y+h//2-bomb_check_area):min(rgb_image.shape[0], y+h//2+bomb_check_area),
                                           max(0, x+w//2-bomb_check_area):min(rgb_image.shape[1], x+w//2+bomb_check_area)]
                    
                    for bomb_color in bomb_colors:
                        lower_bomb = np.array([max(0, c - tolerance) for c in bomb_color])
                        upper_bomb = np.array([min(255, c + tolerance) for c in bomb_color])
                        
                        bomb_mask = cv2.inRange(small_area, lower_bomb, upper_bomb)
                        
                        # If any bomb-like color is detected in the 5x5 area, skip clicking
                        if cv2.countNonZero(bomb_mask) > 0:
                            bomb_detected = True
                            break
                    
                    if not bomb_detected:
                        click_positions.append((center_x, center_y))
        
        if click_positions:
            pyautogui.PAUSE = 0
            for pos in click_positions:
                pyautogui.click(pos[0], pos[1])
                last_positions.append(pos)
        
        time.sleep(0.0005)
    
    messagebox.showinfo("Script Finished", "The script has completed its run.")

# GUI Layout
root.title("Flower Clicker")
root.geometry("300x200")

select_area_button = tk.Button(root, text="Select Area", command=select_area)
select_area_button.pack(pady=10)

area_label = tk.Label(root, text="Selected area: None")
area_label.pack(pady=10)

start_script_button = tk.Button(root, text="Start Script", command=start_script)
start_script_button.pack(pady=10)

root.mainloop()
