'''
This program requires a brief knowledge of L*a*b color space (CIELAB color space) 
'''

'''
In order to label and tag regions of an image as containing a certain
certain color, the Euclidean distance between dataset of known colors
and the averages of a particular image region is to be computed.
The known color that minimizes the Euclidean distance will be chosen as the color identification.
'''

'''
|--- color
|	 |--- __init__.py
|	 |--- colorlabeler.py
|	 |--- shapedetector.py
|--- detect_color.py
|--- example_shapes.png
'''

#import the neccessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
	def __init__(self):
		#initialise the colors dictonary, containing the color
		# name as the key and the RGB tuple as the value
		colors = OrderedDict({
			"red": (255, 0, 0),
			"green": (0, 255, 0),
			"blue": (0, 0, 255)
			})

		# allocate memory for the L*a*b image, then initialise
		# the colour names list
		self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
		self.colorNames = []

		# loop over the colors dictionary
		for (i, (name, rgb)) in enumerate(colors.items()):
			# update the L*a*b array and the color names list
			self.lab[i] = rgb
			self.colorNames.append(name)

		# convert the L*a*b array from the RGB color space
		# to L*a*b
		self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

	def label(self, image, c):
		# construct a mask for the contour, then compute the
		# average L*a*b value for the masked region
		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.erode(mask, None, iterations=2)
		mean = cv2.mean(image, mask=mask)[:3]

		# initialize the minimum distance found thus far
		minDist = (np.inf, None)

		#loop over the known L*a*b color values
		for (i, row) in enumerate(self.lab):
			# computer the distance between the current L*a*b
			# color balue and the mean of the image
			d = dist.euclidean(row[0], mean)

			# if the distance is smaller than the current distance,
			# then update the book-keeping variable
			if d < minDist[0]:
				minDist = (d, i)

		# return the name of the colour with the smallest distance
		return self.colorNames[minDist[1]]


