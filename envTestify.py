import numpy as np
import cv2
import sys

print "The Python version is %s.%s.%s" % sys.version_info[:3]

img = cv2.imread('./images/black.jpg', 0)
rows, cols = img.shape[:2]
#print rows, cols
if (rows == 600 and cols == 800):
	print "Successful Environment Setup!"