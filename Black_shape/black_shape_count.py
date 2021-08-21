'''
1) Recognize only figures with the balck background
2) If 2 or more figures overlap they all should be treated as one object
3) Detect and draw contours around each of the black shapes
'''

#import the necessary packages
import numpy as np
import argparse
import imutils
import cv2

#construct the argument pare and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file", required=True)
ap.add_argument("-o", "--output", help="path to the output image", required=True)
args = vars(ap.parse_args())

#load the image
image = cv2.imread(args["image"])

#find shapes in Images using Python and OpenCV
lower = np.array([0, 0, 0])
upper = np.array([15, 15, 15])
shapeMask = cv2.inRange(image, lower, upper)

#find the contours in the mask
cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print("I have found {} black shapes".format(len(cnts)))

#loop over the contours
for c in cnts:
	#draw the contour and show it
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	
cv2.imshow("Image", image)
cv2.waitKey(0)

cv2.imwrite(args["output"], shapeMask)
