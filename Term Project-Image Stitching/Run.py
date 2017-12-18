import cv2
import imutils
from Bin.Stitching import Stitcher

imageA = cv2.imread('/Samples/1.JPG')
imageB = cv2.imread('/Samples/2.JPG')
imageA = imutils.resize(imageA, width=640)
imageB = imutils.resize(imageB, width=640)

# stitch the images together to create a panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

# show the images
cv2.imshow("Keypoint Matches", vis)
cv2.imshow("Result", result)
cv2.imwrite('output.jpg',result)
cv2.waitKey(0)