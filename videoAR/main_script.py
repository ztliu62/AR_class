import numpy as np
import cv2

def generateHomography(model, target, currframe):
	frame = cv2.cvtColor(currframe, cv2.COLOR_BGR2GRAY)
	model = model

	orb = cv2.ORB_create(500)
	kp_model, desc_model = orb.detectAndCompute(model, None)
	kp_frame, desc_frame = orb.detectAndCompute(frame, None)

	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	rawMatches = bf.match(desc_model, desc_frame)
	sortedMatch = sorted(rawMatches, key = lambda x: x.distance)
	matches = sortedMatch[:100]

	model_pts = np.float32([kp_model[m.queryIdx].pt for m in matches])
	frame_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches])
	homography, mask = cv2.findHomography(model_pts, frame_pts, cv2.RANSAC, 5.0)

	h, w = model.shape
	h_frame, w_frame = frame.shape
	h_target, w_target = target_color.shape[:2]

	pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
	dst = cv2.perspectiveTransform(pts, homography)
	'''
	f_color = np.copy(frame_color)
	f_color = cv2.polylines(f_color, [np.int32(dst)], True, (0,0,255), 3, cv2.LINE_AA) 
	f_color = cv2.drawMatches(model_color, kp_model, f_color, kp_frame, matches, 0, flags = 2)
	cv2.imwrite('match.jpg', f_color)
	'''
	target_pts = np.float32([[0, 0], [0, h_target - 1], [w_target - 1, h_target - 1], [w_target - 1, 0]]).reshape(-1, 1, 2)
	M = cv2.getPerspectiveTransform(target_pts, dst)
	target_warp = cv2.warpPerspective(target_color, M, (w_frame, h_frame), cv2.INTER_LINEAR)
	#cv2.imwrite('warp.jpg', target_warp)

	window = np.ones((h_frame, w_frame, 3), np.uint8)
	cv2.fillPoly(window, [np.int32(dst)], 0)

	currframe *= window
	outImg = currframe + target_warp
	#cv2.imwrite('output.jpg', outImg)
	return outImg


inputfile = 'videos.avi'
model_color = cv2.imread('./model.png')
target_color = cv2.imread('./target.jpg')
model = cv2.cvtColor(model_color, cv2.COLOR_BGR2GRAY)

outfile = './output/frame%d.jpg'

video = cv2.VideoCapture(inputfile)
ret, frame = video.read()
h, w = frame.shape[:2]

fps = 24
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('./output/Video.avi', fourcc, fps, (w, h))
count = 0
while video.isOpened():
	ret, currframe = video.read()
	print 'Read a new frame:' + str(count)
	if ret:
		#image = cv2.cvtColor(currframe, cv2.COLOR_BGR2GRAY)
		#cv2.imwrite(imgOut%count, currframe)
		warpImg = generateHomography(model, target_color, currframe)
		out.write(warpImg)
		count += 1
	else:
		video.release()
		out.release()

