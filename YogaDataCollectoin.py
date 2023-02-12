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


#Creation of detector object
detector = pm.poseDetector()

#Image to train from
filepath = 'train/leftLunge.png'

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

#Stores angles calculated
angles = []

#Reads the image
img = cv2.imread(filepath)
img = cv2.flip(img, 1)

#Finds pose and position of nodes
img = detector.findPose(img, False)
lmList = detector.findPosition(img, False)

#Calculates the angle between the nodes
for i in nodeJoints:
    angles.append(detector.findAngle(img, i[0], i[1], i[2], True))

#Shows image
cv2.imshow('img' ,img)
cv2.waitKey(0)
print(angles)

#Names the page
name = input("Enter pose name: ")


#Saves it in a csv
f = open('data/yogaPoses.csv', 'a')

writer = csv.writer(f)

writer.writerow(name)
writer.writerow(angles)


#Pushes it to firebase
data = {
    u'pose_name': name,
    u'angles': angles
}

db.collection(u'Pose').document(name).set(data)


