import numpy as np
import cv2
import time
from scipy.spatial.distance import euclidean

from SinglePersonTracking import getAngleList
from SinglePersonTracking import poseDetector

from fastdtw import fastdtw

x = np.array([[1,1], [2,2], [3,3], [4,4], [5,5]])
y = np.array([[2,2], [3,3], [4,4]])
testDistance, testPath = fastdtw(x, y, dist=euclidean)
print(testPath)



# Step 1 - Get angle lists for Input A and Input B

list1 = getAngleList("./Assets/TikTokDance1.mp4")
list2 = getAngleList("./Assets/TikTokDance2.mp4") 

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


print('Length of Path: ' + str(len(path))) # this is equal to the length of the biggest list


# Step 3 - Use Path to get aggregate Standard Deviation Difference per frame!





# Step 4 - Superimpose Input A nodes-only video on top of Input B's video!!


# cap = cv2.VideoCapture(0) # - overloaded



capNode = cv2.VideoCapture("./Assets/TikTokDance1.mp4")
cap = cv2.VideoCapture("./Assets/TikTokDance2.mp4")



pTime = 0
detector = poseDetector()


while True:
    success, img = cap.read()
    success2, img2 = capNode.read()
    # img = ~img
    img = cv2.flip(img, 1)
    img = detector.findPose(img)
    #lmList = detector.findPosition(img, draw=False)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime


    img = cv2.flip(img, 1)

    # cv2.putText(img, "Dance Pose Analysis:", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
    #             (255, 0, 0), 3)


    cv2.imshow("Image", img)

    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break

    # cv2.waitKey(0)
    # break
