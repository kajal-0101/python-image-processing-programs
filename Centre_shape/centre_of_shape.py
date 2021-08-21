'''
The goal of the program is to 
1) detect the outline of each shape in the image
2) computing the center of the contour - also called the centroid of the region

Follwing image processings needs to be done:
1) conversion to grayscale
2) blurring to reduce high frequency noise to make our contour detection process more accurate
3) Binarization of the image. Typically edge detection and thresholding are used for this process. Here, thresholding is being applied.

'''

#import the neccessary packages
import argparse
import imutils
import cv2

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
ap.add_argument("-o", "--output", required=True, help="showing the mask")
args = vars(ap.parse_args())

#load the image, convert it to grayscale, blur it slightly, and threshold it
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the threshold image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	if (M["m00"] != 0):
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
	else:
		cX, cY = 0, 0

	# draw the contour and center of the shape on the image
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.circle(image, (cX,cY), 7, (255, 255, 255), -1)
	cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)

cv2.imwrite(args["output"], thresh)

