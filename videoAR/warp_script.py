import numpy as np
import cv2

model_color = cv2.imread('./model.png')
frame_color = cv2.imread('./output/frame1.jpg')
target_color = cv2.imread('./target.jpg')

model = cv2.cvtColor(model_color, cv2.COLOR_BGR2GRAY)
frame = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create(500)
kp_model, desc_model = orb.detectAndCompute(model, None)
kp_frame, desc_frame = orb.detectAndCompute(frame, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
rawMatches = bf.match(desc_model, desc_frame)
sortedMatch = sorted(rawMatches, key = lambda x: x.distance)
matches = sortedMatch[:50]

model_pts = np.float32([kp_model[m.queryIdx].pt for m in matches])
frame_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches])
homography, mask = cv2.findHomography(model_pts, frame_pts, cv2.RANSAC, 5.0)

h, w = model.shape
h_frame, w_frame = frame.shape
h_target, w_target = target_color.shape[:2]

pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
dst = cv2.perspectiveTransform(pts, homography)

f_color = np.copy(frame_color)
f_color = cv2.polylines(f_color, [np.int32(dst)], True, (0,0,255), 3, cv2.LINE_AA) 
f_color = cv2.drawMatches(model_color, kp_model, f_color, kp_frame, matches, 0, flags = 2)
cv2.imwrite('match.jpg', f_color)

target_pts = np.float32([[0, 0], [0, h_target - 1], [w_target - 1, h_target - 1], [w_target - 1, 0]]).reshape(-1, 1, 2)
M = cv2.getPerspectiveTransform(target_pts, dst)
target_warp = cv2.warpPerspective(target_color, M, (w_frame, h_frame), cv2.INTER_LINEAR)
cv2.imwrite('warp.jpg', target_warp)

window = np.ones((h_frame, w_frame, 3), np.uint8)
cv2.fillPoly(window, [np.int32(dst)], 0)
#print window.shape
#print frame_color.shape

frame_color *= window
outImg = frame_color + target_warp
cv2.imwrite('output.jpg', outImg)

#cv2.imshow('match_frame', frame_color)
#cv2.waitKey(0)