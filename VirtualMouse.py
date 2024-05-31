import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

wCam, hCam = 640, 480
frameR = 100     #Frame Reduction

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)
wSrc, hSrc = pyautogui.size()

while True:
    #1 Find hand Landmarks
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)

    #2 Get the tip of index and middle finger
    if len(lmList):
        x1, y1 = lmList[8][1:]        
        x2, y2 = lmList[12][1:]    

        #3 Check which fingers are up
        fingers = detector.fingersUp()

        cv2.rectangle(frame, (frameR, frameR), (wCam-frameR, hCam-frameR), (0, 255, 255), 2)

        #4 Only Index Finger : Moving Mode
        if fingers[1]==1 and fingers[2]==0:

            #5 Convert Coordinates
            index_x = np.interp(x1, (frameR, wCam-frameR), (0, wSrc))
            index_y = np.interp(y1, (frameR, hCam-frameR), (0, hSrc))

            #6 Smoothen Values
            
            #7 Move Mouse
            pyautogui.moveTo(index_x, index_y)
            cv2.circle(img=frame, center=(x1,y1), radius=12, color=(0, 255, 255))

        #8 Both Index and Middle fingers are up : Clicking Mode
        if fingers[1]==1 and fingers[2]==1:
            
            #9 Find distance between fingers
            # length, frame, _ = detector.findDistance(8, 12, frame)
            # print(length)

            #10 Click Mouse if distance is short
            pyautogui.click()

#11 Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    #12 Display
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)