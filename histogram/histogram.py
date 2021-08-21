# cv2.calcHist(image, channels, mask, histSize, ranges)

# import the neccessary packages
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# load the image and show it
image = cv2.imread(args["image"])
cv2.imshow("image", image)

# Grayscale Histogram
# convert the image to grayscale and create a histogra,
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)
hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
plt.figure()
plt.title("Grayscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of Labels")
plt.plot(hist)
plt.xlim([0, 256])

# Color "flattened" histogram
# grab the image channels, initialize the tuple of colors,
# the figure and the flattened feature vector

chans = cv2.split(image)
colors = ('b', 'g', 'r')
plt.figure()
plt.title("'Flattened' color histogram")
plt.xlabel("Bins")
plt.ylabel("# of Pixels")
features = []

# loop over the image channels
for (chan, color) in zip(chans, colors):
	# create a histogram for the current channel and
	# concatenate the resulting histograms for each
	# channel
	hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
	features.extend(hist)

	# plot the histogram
	plt.plot(hist, color = color)
	plt.xlim([0, 256])
plt.show()
# here we are simply showing the dimenisionality of the
# flattened color histogram 256 bins for each channel
# x 3 channels = 768 total values -- in practice, we would
# normally not use 256 bins for each channel, a choice
# between 32-96 bons are normally used, but this tends
# to be application dependent

print("flattened feature vector size: %d" %(np.array(features).flatten().shape))
