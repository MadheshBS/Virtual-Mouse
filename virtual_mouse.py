import cv2 as cv
import numpy as np
import handmodule2 as htm
import time
import autopy
import pyautogui

wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
prevX_scroll = 0
prevY_scroll = 0
prevZoomDist = 0
lastClickTime = 0

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxhands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

while True:
    #Find hand Landmarks
    isTrue, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    #Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        #Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)
        #Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
        #Convert Coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            #Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(wScr - clocX, clocY)
            cv.circle(img, (x1, y1), 15, (255, 255, 255), cv.FILLED)
            plocX, plocY = clocX, clocY

        #Left Clicking Mode and Double clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            
            if length < 40:
                cv.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), -1)
                currentTime = time.time()

                if currentTime - lastClickTime < 0.6:
                    autopy.mouse.click()
                    autopy.mouse.click()   # double click
                    lastClickTime = 0      # reset
                else:
                    autopy.mouse.click()   # single click
                    lastClickTime = currentTime
                time.sleep(0.3) 
        
        #Right Clicking Mode
        if fingers[1] == 1 and fingers[4] == 1 and fingers[2] == 0:
            pyautogui.rightClick()
            time.sleep(0.3)

        # Scrolling Mode
        if fingers[2] == 1 and fingers[1] == 0:
            x, y = x2, y2

            if prevY_scroll != 0:
                diffY = prevY_scroll - y
                diffX = x - prevX_scroll

                # Vertical scroll
                if abs(diffY) > 6:
                    scrollAmount = int(diffY * 1.5)  #To amplify movement
                    pyautogui.scroll(scrollAmount)

                # Horizontal scroll
                if abs(diffX) > 6:
                    scrollAmount = int(diffX * 1.5)
                    pyautogui.hscroll(scrollAmount)

            prevX_scroll = x
            prevY_scroll = y
        else:
            prevX_scroll = 0
            prevY_scroll = 0

        #Zoom in and Zoom out
        if fingers[0] == 1 and fingers[1] == 1:
            zoomDist, img, _ = detector.findDistance(4, 8, img)

            if prevZoomDist != 0:
                diff = zoomDist - prevZoomDist
                if abs(diff) > 10:
                    if diff > 0:
                        pyautogui.hotkey('ctrl', '=')   # Zoom In
                    else:
                        pyautogui.hotkey('ctrl', '-')   # Zoom Out
                    time.sleep(0.5) 
            prevZoomDist = zoomDist
        else:
            prevZoomDist = 0

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (20, 50), cv.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    cv.imshow('Image', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
