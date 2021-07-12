"""
This file is using the the PoseModuel - findAngle function to find the right arm angle of the video capture.
"""
import cv2
import mediapipe as mp
import time
from PoseModule import poseDetector

cap = cv2.VideoCapture(0) #Create the video capture object

pTime = 0 #previous time

detector = poseDetector() #Create the detector object based on the class above
    
while True:
    sucess, img = cap.read()

    img = detector.findPose(img)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        angle = detector.findAngle(img,12,14,16) #Right arm dots
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, color=(255,0,255), thickness=3) #Display the FPS on the screen, agruments at https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/

    cv2.imshow("Image", img)
    cv2.waitKey(1)