'''
|--- color
|	 |--- __init__.py
|	 |--- colorlabeler.py
|	 |--- shapedetector.py
|--- detect_color.py
|--- example_shapes.png
'''

# import thr neccessary packages
from color.shapedetector import ShapeDetector
from color.colorlabeler import ColorLabeler
import argparse
import numpy as np
import imutils
import cv2

# construct the argument and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it ti a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# blur the resized image slightly, then convert it to both
# grayscale and the L*a*b color space
blurred = cv2.GaussianBlur(resized, (5,5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

#initialise the shape detector and color labeler
sd = ShapeDetector()
cl = ColorLabeler()

# loop over the contours
for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	if (M["m00"] != 0):
		cX = int((M["m10"] / M["m00"]) * ratio)
		cY = int((M["m01"] / M["m00"]) * ratio)
	else:
		cX, cY = 0, 0

	# detect the shape of the contour and label the color
	shape = sd.detect(c)
	color = cl.label(lab, c)

	# multiply the contour (x, y) -- coordinates by the resize ratio,
	# then draw the contours and the name of the shape and labeled
	# color on the image
	c = c.astype(np.float_)
	c *= ratio
	c = c.astype(np.int32)
	text = "{} {}".format(color, shape)
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 2 )

# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

'''
One of the primary drawbacks to using this method to label colors is that due to lighting conditions, along with
various hues and saturations, colors rarely look like pure red, green, blue etc.

Identifying small sets of colors using L*a*b color space and the 
Euclidean distance can be done, but for larger color palettes, this metjod will likely return
incoreect results depending on the complexity of the input images

This method works for small color sets in semi controlled lighting conditions, it will likely not work for larger color palletes in
less controlled environments.

'''

'''
python detect_color.py --image example.jpg
'''
