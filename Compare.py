import time
import cv2
import numpy as np
import pyshine as ps
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

from SinglePersonTracking import getAngleList
from SinglePersonTracking import poseDetector
from PercentError import compare_angle_lists


x = np.array([[1,1], [2,2], [3,3], [4,4], [5,5]])
y = np.array([[2,2], [3,3], [4,4]])
testDistance, testPath = fastdtw(x, y, dist=euclidean)
print(testPath)


# Step 1 - Get angle lists for Input A and Input B

list1 = getAngleList("Assets/TikTokDance1.mp4")
list2 = getAngleList("Assets/TikTokDance2.mp4")

print('\n\n Printing List1:   ')
print(list1)

print('\n Printing List2:   ')
print(list2)

print('Done with Step 1 in Compare.py!!')

print('\n\n\n\n\n\n\n')

print('Length of List1: ' + str(len(list1)))
print('Length of List2: ' + str(len(list2)))


# Step 2 - Pass through Dynamic Time Wraping (DTW) Algorithm

distance, path = fastdtw(np.array(list1), np.array(list2), dist=euclidean)

print('\n---------Printing Path Array (Index Match Ups)---------')
print(path)


print('Length of Path: ' + str(len(path))) # this is equal to or greater than (why?) the length of the biggest list


# Step 3 - Use Path to get aggregate Percent Error Difference per frame!

result = compare_angle_lists(list1, list2, path)

percentErrorList = result[0]
flaggedTimeStamps = result[1]
danceScore = abs(100 - round(result[2], 2))

print('\n\nPercentErrorList: ')
print(percentErrorList)

print('\n\nFlaggedTimeStamps: ')
print(flaggedTimeStamps)

print('\n\nDance Score: ')
print(danceScore)


# Step 4 - Superimpose Input A nodes-only video on top of Input B's video!!

detector = poseDetector()

cap1 = cv2.VideoCapture("Assets/TikTokDance1.mp4")
cap2 = cv2.VideoCapture("Assets/TikTokDance2.mp4")

width1  = cap1.get(3)
height1 = cap1.get(4)

while True:

    success1, img1 = cap1.read()
    success2, img2 = cap2.read()

    if not success1:
        break

    img1 = detector.findPose(img1)
    if success2:
        img2 = detector.superimpose(img2, img1)

    ps.putBText(img1, f"Dance Score: {danceScore}", text_offset_x=20, text_offset_y=20, vspace=10, hspace=10, font_scale=2.0,
                background_RGB=(0, 0, 0), text_RGB=(255, 255, 255))

    cv2.imshow("Image", img1)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break