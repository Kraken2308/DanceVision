import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import pandas as pd
import os
import PoseModule as pm
import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


#Logging into firebase
cred = credentials.Certificate("data/dancevision-4b370-firebase-adminsdk-vff02-b33fe2023d.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

pose_ref = db.collection(u'Pose')

docs = db.collection(u'Pose').stream()

#Which angles will be captured
nodeJoints = [
    [13,11,23],
    [15,13,11],
    [14,12,24],
    [16,14,12],
    [11,23,25],
    [23,25,27],
    [25,27,31],
    [12,24,26],
    [24,26,28],
    [26,28,32],
]

#Will store all the poses
pose_list = []

#For loop adding to the pose list 
for doc in docs:
    pose_list.append(doc.to_dict())
    # print(f'{doc.id} => {doc.to_dict()}')
print(pose_list)

#Will store warmup poses
warmup_list = []

#List of warmup poses we want
warmup_name_list = [
    'Right Lunge',
    'Left Lunge',
]


#Creates the list with angles
for pose in pose_list:
    if pose['pose_name'] in warmup_name_list:
        warmup_list.append(pose)
        
print("<--------------------->")

for warmup in warmup_list:
    print(warmup['pose_name'])

#Getting video input from user's webcam
cap = cv2.VideoCapture(0)

#tracks pose number:
pose_number = 0

#stores instance angles
instance_angles = [0] * 10

#sets testing angles
test_angles = []

for warmup in warmup_list:
    test_angles.append(warmup['angles'])

print(test_angles)

#Instantiating pose detector
detector = pm.poseDetector()

#Storing example pose images
leftLunge = cv2.imread('data/leftLunge.png')
leftLunge = cv2.resize(leftLunge, (300, 300))

rightLunge = cv2.imread('data/rightLunge.png')
rightLunge = cv2.resize(rightLunge, (300, 300))

#Setup for overlay
leftLung2gray = cv2.cvtColor(leftLunge, cv2.COLOR_BGR2GRAY)
rightLunge2gray = cv2.cvtColor(rightLunge, cv2.COLOR_BGR2GRAY)

leftLungRet, leftLungMask = cv2.threshold(leftLung2gray, 1, 255, cv2.THRESH_BINARY)
rightLungeRet, rightLungeMask = cv2.threshold(rightLunge2gray, 1, 255, cv2.THRESH_BINARY)

#Checks if user is matching the pose given
def checkmatch(instance_angles, test_angles, confidence = 0.05):
    for idx in (8, 7, 5, 4):
        if not (int(test_angles[idx] * (1 - confidence)) <= instance_angles[idx] <= int(test_angles[idx] * (1 + confidence))):
            return False
    
    # for idx, val in enumerate(instance_angles):
    #     if not (int(test_angles[idx] * (1 - confidence)) <= val <= int(test_angles[idx] * (1 + confidence))):
    #         return False

    return True

#While loop iterating while the user is warming up
while pose_number < len(warmup_list):
    
    #Reading camera input
    success, img = cap.read()
    if not success:
        print("Ignoring empty frame")
        continue
    
    #Resizing image
    img = cv2.resize(img, (1280, 720))
    
    #flip image horizontally to mirror user
    img = cv2.flip(img, 1)
    
    #Shows the user the nodes and finds their pose
    img = detector.findPose(img, draw = False)
    lmList = detector.findPosition(img, draw = False)

    #SHOWS FULL BODY ANGLES
    if len(lmList) != 0:
        for i in range(len(nodeJoints)):
            instance_angles[i] = (detector.findAngle(img, nodeJoints[i][0],
                                                     nodeJoints[i][1], nodeJoints[i][2], True, True))
            
    if checkmatch(instance_angles, test_angles[pose_number]):
        pose_number += 1
            
    leftLungeROI = img[-300-10:-10, -300-10:-10]
    rightLungeROI = img[-300-10:-10, -300-10:-10]
    
    #Sets the pose in the corner to which pose is needed
    if pose_number == 0:
        leftLungeROI[np.where(leftLungMask)] = 0
        leftLungeROI += leftLunge
        
        #Adding text
        cv2.putText(img, 'Step: ' + str(pose_number + 1), (970, 400), cv2.FONT_HERSHEY_PLAIN, 4,
                    (0, 0, 255), 4)
        
        cv2.putText(img, 'Lunge Right!', (50, 50), cv2.FONT_HERSHEY_PLAIN, 4,
                    (0, 0, 255), 4)
        
        
    elif pose_number == 1:
        rightLungeROI[np.where(rightLungeMask)] = 0
        rightLungeROI += rightLunge
        
        #Adding text
        cv2.putText(img, 'Step: ' + str(pose_number + 1), (970, 400), cv2.FONT_HERSHEY_PLAIN, 4,
                    (0, 0, 255), 4)
        
        cv2.putText(img, 'Lunge Left!', (50, 50), cv2.FONT_HERSHEY_PLAIN, 4,
                    (0, 0, 255), 4)
        
    print(pose_number)
        
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    