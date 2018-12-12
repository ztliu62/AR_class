import numpy as np
import cv2 
import matplotlib.pyplot as plt

# read file in as gray-scale image
gray_img = cv2.imread('./Images/white.jpg', 0)
# read file in as color-scale image
color_img = cv2.imread('./Images/black.jpg', 1)

# write image to file
cv2.imwrite('./output/white_output.jpg', gray_img)
cv2.imwrite('./output/black_color.jpg', color_img)

# display images
cv2.imshow('color_file', color_img)
cv2.waitKey(0)

# Display color channel 
plt.figure(figsize = (36,12))
plt.subplot(131)
plt.imshow(color_img[:,:,0], cmap = 'gray')
plt.title('Blue')
plt.subplot(132)
plt.imshow(color_img[:,:,1], cmap = 'gray')
plt.title('Green')
plt.subplot(133)
plt.imshow(color_img[:,:,2], cmap = 'gray')
plt.title('Red')
plt.savefig('./output/Color_Channel.png')
plt.show()

# Image Information
img = np.copy(color_img)
img_dims = img.ndim
img_shape = img.shape
img_size = img.size

print "\n{:^70}".format("NDARRAY ATTRIBUTES")
print "{:^70}\n".format("====================")
print "{:^30}{:^20}{:^20}".format("Description", "Example", "Value")
print "{:^30}{:^20}{:^20}".format("-------------", "---------", "-------")
print "{:^30}{:^20}{:^20}".format("Number of dimensions", "img.ndim", img_dims)
print "{:^30}{:^20}{:^20}".format("Image Shape", "img.shape", img_shape)
print "{:^30}{:^20}{:^20}".format("Pixel count", "img.size", img_size)
 
# Image Manipulation
bluePlusGreen = color_img[:,:,0] + color_img[:,:,1]
plt.figure(figsize=(12,12))
plt.imshow(bluePlusGreen, cmap = 'gray')
plt.show()

img = color_img.astype(float)
bluePlusGreen = img[:,:,0] + color_img[:,:,1]
plt.figure(figsize=(12,12))
plt.imshow(bluePlusGreen, cmap = 'gray')
plt.show()

# Image Blending
black_img = cv2.imread('./Images/black.jpg').astype(float)
white_img = cv2.imread('./Images/white.jpg').astype(float)
alpha = cv2.imread('./Images/mask.jpg').astype(float)

alpha = cv2.GaussianBlur(alpha, (51,51), 0)
alpha = alpha/255.

rows, cols = black_img.shape[:2]
forground = alpha*black_img
background = (1.0-alpha)*white_img

outImg = foreground + background
cv2.imwrite('./output/blend.jpg', outImg)