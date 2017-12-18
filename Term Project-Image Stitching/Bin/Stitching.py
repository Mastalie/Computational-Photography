import numpy as np
import cv2

# print(cv2.__version__)
# Require OpenCV 3.x
# opencv_contrib is not built-in in OpenCV, requires to pip install python-opencv-contrib in the enviroment

class Stitcher:

    def __init__(self):
        pass

    def stitch(self, images, ratio=0.75, reprojThresh=4.0,
               showMatches=False):

        # ratio: David Lowe Test
        # reprojThresh: value for RANSAC
        # unpack the images, then detect keypoints and extract local invariant descriptors from them
        # and match features between the two images
        (imageB, imageA) = images
        (keypointsA, featuresA) = self.detectAndDescribe(imageA)
        (keypointsB, featuresB) = self.detectAndDescribe(imageB)

        M = self.matchKeypoints(keypointsA, keypointsB, featuresA, featuresB, ratio, reprojThresh)

        # otherwise, apply a perspective warp to stitch the images

        (matches, H, status) = M
        result = cv2.warpPerspective(imageA, H,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        # check to see if the keypoint matches should be visualized
        if showMatches:
            vis = self.drawMatches(imageA, imageB, keypointsA, keypointsB, matches, status)
            # return a tuple of the stitched image and the
            # visualization
            return (result, vis)
        # return the stitched image
        return result


    def detectAndDescribe(self, image):

        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # use Difference of Gaussian (DoG) or SIFT(here)
        # detect and extract features from the image
        descriptor = cv2.xfeatures2d.SIFT_create()
        (keypoints, features) = descriptor.detectAndCompute(image, None)

        # convert the keypoints from KeyPoint objects to NumPy arrays
        keypoints = np.float32([kp.pt for kp in keypoints])

        # return a tuple of keypoints and features
        return (keypoints, features)


    def matchKeypoints(self, keypointsA, keypointsB, featuresA, featuresB,
                       ratio, reprojThresh):

        # compute the raw matches and initialize the list of actual matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        # computing a homography requires at least 4 matches
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([keypointsA[i] for (_, i) in matches])
            ptsB = np.float32([keypointsB[i] for (i, _) in matches])
            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                                             reprojThresh)
            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (matches, H, status)
        # otherwise, no homograpy could be computed
        return None


    def drawMatches(self, imageA, imageB, keypointsA, keypointsB, matches, status):
        # initialize the output visualization image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully
            # matched
            if s == 1:
                # draw the match
                ptA = (int(keypointsA[queryIdx][0]), int(keypointsA[queryIdx][1]))
                ptB = (int(keypointsB[trainIdx][0]) + wA, int(keypointsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
        # return the visualization
        return vis
