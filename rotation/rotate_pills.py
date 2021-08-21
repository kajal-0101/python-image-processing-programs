# definition of rotate_bound from imutils

#def rotate_bound(image, angle):
#	# grab the dimensions of the image and then determine the center
#	(h, w) = image.shape[:2]
#	(cX, cY) = (w//2, h//2)

	# grab the rotation matrix (applying the negative of the)
	# angle to rotate clockwise), then grab the sine and cosine
	# (i.e., the rotation components of the matrix)

#	M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
#	cos = np.abs(M[0, 0])
#	sin = np.abs(M[0, 1])

	# compute the new bounding dimensions of the image
#	nW = int((h * sin) + (w * cos))
#	nH = int((h * cos) + (w * sin))

	# adjust the rotation matrix to take into account translation
#	M[0, 2] += (nW / 2) - cX
#	M[1, 2] += (nH / 2) - cY

	# perform the actual rotation and return the image
#	return cv2.warpAffine(image, M, (nW, nH))

# ------ EXplaination of the above function ------
# The method accepts an imput image and an angle to rotate it
# It is assumed that the image will be rotated about its center (x, y) co-ordinates
# cv2.getRotationMatrix2D is called to obtain the rotation matrix M
# To resolve the border cut issue, collect the cosine and sine values from the rotation matrix M
# This enables to compute the new width and height of the rotated image, to ensure no part of the image is cut off
# once the new width and height is calculated, the rotation matrix is modified by adjusting the translation
# Finally, cv2.warpAffine is called to rotate the actual image using OPenCV while ensuring none of the image is cut off
# -------------------------------------------------- 



# import the neccessary packages
import numpy as np
import argparse
import imutils
import cv2

# construct the argument and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the image file")
args = vars(ap. parse_args())

# load the image from the disk, convert it to grayscale, blur it,
# and apply egde detection to reveal the outline of the pill
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
edged = cv2.Canny(gray, 20, 100)
#cv2.imshow("edged", edged)
#cv2.waitKey(0)
cv2.imwrite("edged_pill.png", edged)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# ensure at least one contour was found
if (len(cnts) > 0):
	c = max(cnts, key=cv2.contourArea)
	mask = np.zeros(gray.shape, dtype="uint8")
	cv2.drawContours(mask, [c], -1, 255, -1)

	# compute its bounding box of pill, then extract the ROI
	# and apply the mask
	(x, y, w, h) = cv2.boundingRect(c)
	imageROI = image[y:y+h, x:x+w]
	maskROI = mask[y:y+h, x:x+w]
	imageROI = cv2.bitwise_and(imageROI, imageROI, mask=maskROI)
	cv2.imwrite("maskROI_pill.png", maskROI)
	cv2.imwrite("imageROI_pill.png", imageROI)
	cv2.imwrite("mask_pill.png", mask)
	#cv2.imshow("mask", mask)
	#cv2.waitKey(0)

	# loop over the rotation angles
	for angle in np.arange(0, 360, 90):
		rotated = imutils.rotate(imageROI, angle)
		cv2.imshow("Rotated (problematic)", rotated)
		cv2.waitKey(0)

	# loop over the rotation angles again, this time ensure the
	# entire pill is still within the ROI after rotation
	for angle in np.arange(0, 360, 90):
		rotated = imutils.rotate_bound(imageROI, angle)
		cv2.imshow("Rotated (correct)", rotated)
		cv2.waitKey(0)