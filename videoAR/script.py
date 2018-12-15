import numpy as np
import cv2

inputfile = 'videos.mp4'
imgOut = './output/frame%d.jpg'

video = cv2.VideoCapture(inputfile)
ret, frame = video.read()
h, w = frame.shape[:2]

#create output video
fps = 24
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('./output/Video.avi', fourcc, fps, (w, h))
count = 0
while video.isOpened():
	ret, currframe = video.read()
	print 'Read a new frame:' + str(count)
	if ret:
		#image = cv2.cvtColor(currframe, cv2.COLOR_BGR2GRAY)
		cv2.imwrite(imgOut%count, currframe)
		out.write(cv2.flip(currframe,0))
		count += 1
	else:
		video.release()
		out.release()





