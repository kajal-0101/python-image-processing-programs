'''
Tree of the folder
|--- shape
|	 |--- shapedetector.py
|--- detect_shapes.py
|--- shapes_and_colors.png
'''


# import the necessary packages
from shape.shapedetector import ShapeDetector
import argparse
import numpy as np
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the threshold image and initialise the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

# loop over the contours
for c in cnts:
	# compute the centre of the contour, then detect the name of the
	#shape using only the contour
	M = cv2.moments(c)
	if (M["m00"] != 0):
		cX = int(M["m10"] / M["m00"] * ratio)
		cY = int(M["m01"] / M["m00"] * ratio)
	else:
		cX, cY = 0, 0
	shape = sd.detect(c)

	# multiply the contour (x, y) -- coordinated by the resize ratio
	# then draw the contours and the name of the shape on the image
	c = c.astype(np.float_)
	c *= ratio
	c = c.astype(np.int32)
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape, (cX,cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

