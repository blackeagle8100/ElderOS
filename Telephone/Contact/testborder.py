#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:33:09 2023

@author: meme
"""

import cv2
import numpy as np

def remove_black_borders(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Calculate the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Crop the image to remove the black borders
    cropped_image = image[y:y+h, x:x+w]
    
    return cropped_image

# Load the image
image = cv2.imread('./1307891792.png')

# Remove black borders
cropped_image = remove_black_borders(image)

# Display the original and cropped images
cv2.imshow('Original Image', image)
cv2.imshow('Cropped Image', cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()