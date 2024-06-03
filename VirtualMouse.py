import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

wCam, hCam = 640, 480
frameR = 100     #Frame Reduction
smoothening = 3

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

dragging = False
scrolling = False

pyautogui.FAILSAFE = False  # To disable Fail safe(To disable the termination of code when takes cursor to corners)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wSrc, hSrc = pyautogui.size()

try:
    while True:
        #1 Find hand Landmarks
        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)

        #2 Get the tip of index and middle finger
        if len(lmList):
            x1, y1 = lmList[8][1:]  # Index finger tip  
            x4, y4 = lmList[6][1:]

            x2, y2 = lmList[12][1:]  # Middle finger tip
            x5, y5 = lmList[10][1:]

            x3, y3 = lmList[4][1:]   # Thumb tip


            #3 Check which fingers are up
            fingers = detector.fingersUp()

            cv2.rectangle(frame, (frameR, frameR), (wCam-frameR, hCam-frameR), (0, 255, 255), 2)  

            #Find the distance between fingers
            length_i_m, frame, _ = detector.findDistance(8, 12, frame)
            length_t_i, frame, _ = detector.findDistance(4, 8, frame)
            length_t_m, frame, _ = detector.findDistance(4, 12, frame)

            #4 Both Index and Middle fingers are up with a certain distance : Moving Mode
            if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and length_i_m>50:

                #5 Convert Coordinates
                index_x = np.interp(x1, (frameR, wCam-frameR), (0, wSrc))    #(x1, (0, wCam), (0, wSrc))
                index_y = np.interp(y1, (frameR, hCam-frameR), (0, hSrc))    #(y1, (0, wCam), (0, wSrc))


                #6 Smoothen Values
                clocX = plocX + (index_x - plocX)/smoothening
                clocY = plocY + (index_y - plocY)/smoothening


                #7 Move Mouse
                pyautogui.moveTo(clocX, clocY)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(frame, (x1,y1), 12, (0, 255, 255), cv2.FILLED)
                cv2.circle(frame, (x2,y2), 12, (0, 255, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY


            # Index finger is down and middle finger is up : Left click
            if fingers[0]==0 and fingers[1]==0 and fingers[2]==1 and length_i_m>50:
                cv2.circle(frame, (x1,y1), 12, (255, 255, 0), cv2.FILLED)
                pyautogui.click(clicks=1, button='left')


            # Index finger is up and middle finger is down : Right click
            if fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and length_i_m>50:
                cv2.circle(frame, (x2,y2), 12, (255, 255, 0), cv2.FILLED)
                pyautogui.click(clicks=1, button='right')
                

            #9 Distance reduces between index and middle finger : Double Left Click
            if fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and length_i_m<20:
                cv2.circle(frame, (x1,y1), 12, (255, 255, 0), cv2.FILLED)
                pyautogui.click(clicks=2, button='left')


            # Scrolling : 
            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and length_t_i < 40:
                cv2.circle(frame, (x3, y3), 12, (255, 255, 0), cv2.FILLED)
                
                if not scrolling:
                    scrolling = True
                    scroll_start_x, scroll_start_y = x3, y3
                else:
                    scroll_dx = x3 - scroll_start_x
                    scroll_dy = y3 - scroll_start_y

                    scroll_speed = 4

                    if abs(scroll_dy) > abs(scroll_dx):
                        pyautogui.scroll(-scroll_dy * scroll_speed)
                    else:
                        pyautogui.keyDown('shift')
                        pyautogui.keyDown('ctrl')
                        pyautogui.scroll(-scroll_dx * scroll_speed)
                        pyautogui.keyUp('ctrl')
                        pyautogui.keyUp('shift')

                    scroll_start_x, scroll_start_y = x3, y3

            else:
                scrolling = False
            

            # Vertical Scrolling : according to relative positon of thumb and index finger (distance is smaller than a certain value)
            # if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and length_t_i<40:
            #     cv2.circle(frame, (x3,y3), 12, (255, 255, 0), cv2.FILLED)
            #     # Scroll up when tip of thumb is below tip of index
            #     if y3 < y1:
            #         pyautogui.scroll(60)
            #     # Scroll down when tip of thumb is above tip of index
            #     elif y3 > y1:
            #         pyautogui.scroll(-60)



            # if fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 1 and length_t_m<40:
            #     cv2.circle(frame, (x3,y3), 12, (255, 255, 0), cv2.FILLED)
            #     # Scroll up when tip of thumb is below tip of index
            #     if y3 < y2:
            #         pyautogui.hscroll(60)
            #     # Scroll down when tip of thumb is above tip of index
            #     elif y3 > y2:
            #         pyautogui.hscroll(-60)

            
            # Dragging mode : Index and middle finger is down 
            if fingers[1] == 0 and fingers[2] == 0 and length_t_m<25:
                if not dragging:
                    dragging = True
                    pyautogui.mouseDown()
                    # print("Drag started")
                # Convert Coordinates
                index_x = np.interp(x1, (frameR, wCam - frameR), (0, wSrc))
                index_y = np.interp(y1, (frameR, hCam - frameR), (0, hSrc))
                # Smoothen Values
                clocX = plocX + (index_x - plocX) / smoothening
                clocY = plocY + (index_y - plocY) / smoothening
                # Drag the mouse
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY
                cv2.circle(frame, (x1, y1), 12, (0, 0, 255), cv2.FILLED)

            # Stop dragging when index and middle finger are up again
            if fingers[1] == 1 and fingers[2] == 1 and dragging:
                dragging = False
                pyautogui.mouseUp()
                # print("Drag stopped")


        #11 Frame Rate
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

        #12 Display
        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)

except pyautogui.FailSafeException:
    print("Fail-safe triggered! Exiting script.")
