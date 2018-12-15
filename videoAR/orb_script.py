import numpy as np
import cv2

model = cv2.imread('./model.png', 0)
frame = cv2.imread('./output/frame1.jpg', 0)
target = cv2.imread('./target.jpg')
orb = cv2.ORB_create(500)

kp_model, desc_model = orb.detectAndCompute(model, None)
kp_frame, desc_frame = orb.detectAndCompute(frame, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
rawMatches = bf.match(desc_model, desc_frame)
sortedMatch = sorted(rawMatches, key = lambda x: x.distance)
matches = sortedMatch[:100]

if len(matches) > 50:
	model_pts = np.float32([kp_model[m.queryIdx].pt for m in matches])
	frame_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches])

	homography, mask = cv2.findHomography(model_pts, frame_pts, cv2.RANSAC, 5.0)
	h, w = model.shape
	pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
	dst = cv2.perspectiveTransform(pts, homography)
	frame = cv2.polylines(frame, [np.int32(dst)], True, 0, 3, cv2.LINE_AA)  
	frame = cv2.drawMatches(model, kp_model, frame, kp_frame, matches[:100], 0, flags = 2)
	cv2.imshow('frame', frame)
	cv2.waitKey(0)
