"""
This is a test script to looad the class from the PoseModule
"""


import cv2
import mediapipe as mp
import time

from PoseModule import poseDetector

cap = cv2.VideoCapture('Videos/video2.mp4') #Create the video capture object

pTime = 0 #previous time
cTime = 0 #current time

detector = poseDetector() #Create the detector object based on the class above
    
while True:
    sucess, img = cap.read()

    img = detector.findPose(img)
    
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList)
    cTime = time.time()

    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, color=(255,0,255), thickness=3) #Display the FPS on the screen, agruments at https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/

    cv2.imshow("Image", img)
    cv2.waitKey(1)