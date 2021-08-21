# cv2.calcHist(image, channels, mask, histSize, ranges)

# import the neccessary packages
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2


image = cv2.imread("doctor.jpg")
cv2.imshow("image", image)

chans = cv2.split(image)

# 2D Color Histogram
# let's move on to 2D histograms -- I am reducing the
# number of bins in the histograms from 256 to 32 so we
# can better visualize the results
fig = plt.figure()
# plot a 2D color histogram for green and blue
ax = fig.add_subplot(131)
hist = cv2.calcHist([chans[1], chans[0]], [0, 1], None,
	[32, 32], [0, 256, 0, 256])
p = ax.imshow(hist, interpolation = "nearest")
ax.set_title("2D Color Histogram for Green and Blue")
plt.colorbar(p)
# plot a 2D color histogram for green and red
ax = fig.add_subplot(132)
hist = cv2.calcHist([chans[1], chans[2]], [0, 1], None,
	[32, 32], [0, 256, 0, 256])
p = ax.imshow(hist, interpolation = "nearest")
ax.set_title("2D Color Histogram for Green and Red")
plt.colorbar(p)
# plot a 2D color histogram for blue and red
ax = fig.add_subplot(133)
hist = cv2.calcHist([chans[0], chans[2]], [0, 1], None,
	[32, 32], [0, 256, 0, 256])
p = ax.imshow(hist, interpolation = "nearest")
ax.set_title("2D Color Histogram for Blue and Red")
plt.colorbar(p)
plt.show()
# finally, let's examine the dimensionality of one of
# the 2D histograms
print ("2D histogram shape: %s, with %d values" % (
	hist.shape, hist.flatten().shape[0]))