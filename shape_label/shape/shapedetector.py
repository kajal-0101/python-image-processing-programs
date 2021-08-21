'''
Tree of the folder
|--- shape
|	 |--- shapedetector.py
|--- detect_shapes.py
|--- shapes_and_colors.png
'''

'''
detect method requires only a single argument, c, the contour (i.e., outline) of the shape being identified
In order to perform shape detection, contour approximation is being used
Contour approximation is an algorithm for reducing the number of points in a curve with a reduced set of points
This algorithm is commonly known as Ramer-Douglas-Peucker Algorithm, or the split and merge algorithm.
'''
# import the neccessary packages
import cv2

class ShapeDetector:
	def __init__(self):
		pass
		# skiping the constructor since nothing needs to be initialized

	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		# if the shape is a traingle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"

		# if the shape has 4 vertices, it is either a square or a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)

			# a square will have an aspect ratio that is approximately equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"

		# otherwise , we assume the shape is a circle
		else:
			shape = "circle"

		# return the name of the shape
		return shape

'''
Output: 
python detect_shapes.py --image shapes_and_colors.jpg
'''
