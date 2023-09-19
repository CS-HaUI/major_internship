import cv2
import numpy as np

# Create a blank image
image = np.zeros((400, 600, 3), dtype=np.uint8)

# Define text properties
text = "Fancy Text"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2.5
font_color = (255, 255, 255)  # White color in BGR
thickness = 3
line_type = cv2.LINE_AA  # Antialiased line for smoother text rendering

# Calculate text size to center it
(text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
x = (image.shape[1] - text_width) // 2
y = (image.shape[0] + text_height) // 2

# Put the text on the image
cv2.putText(image, text, (x, y), font, font_scale, font_color, thickness, line_type)

# Display the image
cv2.imshow('Fancy Text Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
