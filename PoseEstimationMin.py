import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) #Raad the video'Videos/video2.mp4'
pTime = 0

mpPose = mp.solutions.pose
pose = mpPose.Pose() #Default static_image_mode=False; this is to detect and track the Pose
mpDraw = mp.solutions.drawing_utils #Use this to draw the 

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #The default is BGR for video capture, convert to RGB as mediapipe using RGB
    results = pose.process(imgRGB)

    if results.pose_landmarks: #Pose landmarks are being divided into 32 dots
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape #Get the height, width of the image capture
            cx, cy = int(lm.x*w), int(lm.y*h) #Calculate the normolized position to pixel
            cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
            print(id, cx, cy)
    #Create the FPS tracking
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    
    
    cv2.imshow('Image', img) #Display the video
    cv2.waitKey(1)