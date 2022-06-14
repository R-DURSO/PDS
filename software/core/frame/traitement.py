import numpy as np
import cv2 as cv
import scipy.signal as sp

frame = cv.imread("./pyramide.jpg")
iframe = cv.resize(frame,(320,240))

frame = cv.cvtColor(iframe, cv.COLOR_BGR2GRAY)
ret, frame = cv.threshold(frame, 60, 255, cv.THRESH_BINARY_INV)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
frame = cv.morphologyEx(frame, cv.MORPH_OPEN, kernel, iterations=1)
frame = cv.morphologyEx(frame, cv.MORPH_CLOSE, kernel, iterations=2)

edges = cv.Canny(frame, 50, 150, apertureSize=3)

cv.imshow("frame", edges)
cv.waitKey(0)

# maskX = np.array(
# 	([-1, 0, 1],
# 	[-2, 0, 2],
# 	[-1, 0, 1])
# )

# maskY = np.array(
# 	([-1, -2, -1],
# 	[0, 0, 0],
# 	[1, 2, 1])
# )

# sobelX = sp.convolve(frame, maskX, mode="full")
# sobelY = sp.convolve(frame, maskY, mode="full")

# sobel = np.zeros((len(frame),len(frame[0])))

# for i in range(len(frame)):
# 	for j in range(len(frame[0])):
# 		sobel[i][j] = np.sqrt(sobelX[i][j]**2 + sobelY[i][j]**2)


maxi = maxj = 0
mini = minj = float("inf")

for i in range(len(frame)):
	for j in range(len(frame[0])):
		if edges[i][j] > 40:
			if i > maxi:
				maxi = i
			if i < mini:
				mini = i
			if j > maxj:
				maxj = j
			if j < minj:
				minj = j

print("mini: ", mini, ", maxi: ", maxi, ", minj: ", minj, ", maxj: ", maxj)

# cv.imshow("sobel", sobel)
# cv.waitKey(0)

lines = cv.HoughLines(edges,1,np.pi/180,30)
print(len(lines))
for line in lines:
	for rho,theta in line:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))

		cv.line(iframe,(x1,y1),(x2,y2),(0,0,255),2)

cv.imshow("hough", iframe)
cv.waitKey(0)