"""
James Yan - June 09, 2021 
Creating a class that can be reusable from other project quickly that using the Post track Tech.
The class will creat mpPose object that can process a image or stream image and detect the Pose (body) from the image.
The class wiil create mp.Draw object which will draw the dots/connection on the detected Pose within the images.
"""

import cv2
import mediapipe as mp
import time

class poseDetector():
    def __init__(self, mode=False, complexity=1, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.detectionCon, self.trackCon) # creating the pose object
        self.mpDraw = mp.solutions.drawing_utils #This is built drawing function to draw dots/connections of the tracked hand landmarks (21 dots per hand)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #By default, cap.read() ussing cv2.VideoCapture is captureing BGR for color order; converting to RGB
         
        #Process the Pose from the image (video capture), the results are tracking the Pose from video capture
        #Make result a var with in the self, so it can be used again.
        self.results = self.pose.process(imgRGB)
        
        if self.results.pose_landmarks: #If hands detected
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(self.results.pose_landmarks.landmark):
                    h, w, c = img.shape #Get the height, width of the image capture
                    cx, cy = int(lm.x*w), int(lm.y*h) #Calculate the normolized position to pixel
                    cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
                    print(id, cx, cy)
        return img

    def findPosition(self, img, draw = True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape #Get the height, width of the image capture
                cx, cy = int(lm.x*w), int(lm.y*h) #Calculate the normolized position to pixel
                #if draw: cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED) #This can highlight the certain dots on the body
                lmList.append([id,cx,cy]) #Append the dots of the body position in to the list.
        return lmList

# A main() function that can be run itself.
def main():

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

if __name__ == "__main__":
    main()