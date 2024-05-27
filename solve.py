import cv2
import numpy as np
from matplotlib import pyplot as plt

def increase_sharpness(image):
    # Define the sharpening kernel
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    # Apply the sharpening kernel to the image
    sharpened_image = cv2.filter2D(image, -1, kernel)
    return sharpened_image
def increase_saturation(image, factor):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Split the channels
    h, s, v = cv2.split(hsv)
    # Increase the saturation channel
    s = np.clip(s * factor, 0, 255).astype(np.uint8)
    # Merge the channels back
    enhanced_hsv = cv2.merge([h, s, v])
    # Convert back to BGR color space
    enhanced_image = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)
    return enhanced_image
def hex_to_rgb(hex_code):
    # Remove '#' if present
    if hex_code.startswith('#'):
        hex_code = hex_code[1:]

    # Convert hex to RGB
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)

    return (r, g, b)
def closest_basic_color(rgb):
    r, g, b = rgb
    
    # Define thresholds for each basic color
    red_threshold = 75
    green_threshold = 75
    blue_threshold = 75
    
    
    # Check if the color is closer to red
    if r > red_threshold and g < green_threshold and b < blue_threshold:
      if r - g > 50 and g - b > 50 and r > 150:
        return "orange"
      else:
        return "red"
    # Check if the color is closer to green
    elif r < red_threshold and g > green_threshold and b < blue_threshold:
        return "green"
    elif g - r > 150 and b < 150:
        return "green"
    # Check if the color is closer to blue
    elif r < red_threshold and g < green_threshold and b > blue_threshold:
        return "blue"
    elif 50 < g - r  < 120 and 100 < b:
        return "blue"
    # Check if the color is closer to orange
    elif r - g > 50 and g - b > 50 and r > 180:
        return "orange"
    # Check if the color is closer to yellow
    elif r - g > 50 and g - b > 50 and r < 200 and r > 100 and g < r - 50:
        return "yellow"
    elif r - g < 30 and b < 100:
        return "yellow"
    # Check if the color is closer to white
    elif r > 120 and g > 120 and b > 120:
        return "white"
    # If none of the above, return the closest basic color based on the Euclidean distance
    else:
        distances = {
            'red': (r - 255) * 2 + g * 2 + b ** 2,
            'green': r * 2 + (g - 255) * 2 + b ** 2,
            'blue': r * 2 + g * 2 + (b - 255) ** 2,
            'orange': (r - 255) * 2 + (g - 165) * 2 + b ** 2,
            'yellow': (r - 255) * 2 + (g - 255) * 2 + b ** 2,
            'white': (r - 255) * 2 + (g - 255) * 2 + (b - 255) ** 2
        }
        return min(distances, key=distances.get)
def color_to_letter(color_array):
    color_mapping = {
        'green': 'D',
        'blue': 'U',
        'red': 'L',
        'white': 'F',
        'orange': 'R',
        'yellow': 'B'
    }
    
    output = []
    
    for color in color_array:
        if color in color_mapping:
            output.append(color_mapping[color])
    
    return output

def get_letters(filename):
    # Load the image
    img = cv2.imread("uploads/"+filename)

    # Increase image sharpness
    sharpened_img = increase_sharpness(img)

    # Increase color strength
    enhanced_img = increase_saturation(sharpened_img, 1.5)  # Adjust the factor as needed

    # Define the number of rows and columns for the grid
    num_rows = 3
    num_cols = 3

    # Calculate the size of each box
    height, width, _ = enhanced_img.shape
    box_height = height // num_rows
    box_width = width // num_cols

    # Initialize a list to store average colors
    average_colors = []

    # Loop through the grid and draw rectangles
    for i in range(num_rows):
        for j in range(num_cols):
            # Calculate the coordinates of the box
            start_x = j * box_width
            start_y = i * box_height
            end_x = (j + 1) * box_width
            end_y = (i + 1) * box_height
            
            # Draw a rectangle on the enhanced image
            cv2.rectangle(enhanced_img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            
            # Extract the pixels within the box region
            box_region = enhanced_img[start_y:end_y, start_x:end_x]
            
            # Calculate the average color in the box region
            average_color = np.mean(box_region, axis=(0, 1))
            
            # Store the average color
            average_colors.append(average_color)

    plt.figure(figsize=(8, 6))
    # Convert BGR to RGB for display
    enhanced_img_rgb = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2RGB)
    # Plot the enhanced image
    plt.imshow(enhanced_img_rgb)

    # Convert the average colors to RGB format and then to hexadecimal
    hex_colors = ['#{:02x}{:02x}{:02x}'.format(int(color[2]), int(color[1]), int(color[0])) for color in average_colors]

    # Re-run the previous code to populate COLORNAMES array with the updated logic

    # Array to store color names
    COLORNAMES = []

    # Iterate over each hex color, convert to RGB, get color name, and append to COLORNAMES array
    for hex_color in hex_colors:
        rgb_color = hex_to_rgb(hex_color)
        color_name = closest_basic_color(rgb_color)
        COLORNAMES.append(color_name)

    result = color_to_letter(COLORNAMES)
    return result