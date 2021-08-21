# Rotate images (correctly) with OpenCV and Python using imutils library

# import the neccessary packages
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image file")
args = vars(ap.parse_args())

# load the image from disk
image = cv2.imread(args["image"])

# loop over the rotation angles
for angle in np.arange(0, 360, 60): # looping form 0 to 360 degrees with an interval of 60 degrees
	rotated = imutils.rotate(image, angle)
	cv2.imshow("Rotated (Problematic)", rotated)
	cv2.waitKey(0)

# loop over the rotation angles again, this time ensuring
# no part of the image is cut off
for angle in np.arange(0, 360, 60):
	rotated = imutils.rotate_bound(image, angle)
	cv2.imshow("Rotated (Correct)", rotated)
	cv2.waitKey(0)
