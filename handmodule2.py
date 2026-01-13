# Hand Tracking Module
# Adapted from freeCodeCamp.org Computer Vision Tutorial
# Original implementation uses MediaPipe Hands
# Used here for educational purposes

import cv2 as cv
import mediapipe as mp
import time 
import math

class handDetector():
    def __init__(self,mode=False,maxhands=2,detectCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxhands = maxhands
        self.detectCon = detectCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,max_num_hands=self.maxhands, min_detection_confidence=self.detectCon,min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]

    def findHands(self,img,draw=True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                
                if draw:                   
                    self.mpDraw.draw_landmarks(img,handlms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0,draw=True):
        self.lmlist =[]
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myhand.landmark):
                        #print(id,lm)
                        h,w,c = img.shape
                        cx, cy = int(lm.x*w),int(lm.y*h)
                        self.lmlist.append([id,cx,cy])
                        #print(id,cx,cy)
                        #if id == 4:
                        if draw:
                            cv.circle(img,(cx,cy),10,(255,255,0),-1)
        return self.lmlist
    
    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[4]][1]:  #For right hand
            if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        elif self.lmlist[self.tipIds[0]][1] > self.lmlist[self.tipIds[4]][1]:  #For left hand
            if self.lmlist[self.tipIds[0]][1] > self.lmlist[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)        
        # 4 Fingers
        for id in range(1, 5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        totalFingers = fingers.count(1)
        #print(totalFingers)
        return fingers
    
    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):
        x1, y1 = self.lmlist[p1][1:]
        x2, y2 = self.lmlist[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv.circle(img, (x1, y1), r, (255, 0, 255), -1)
            cv.circle(img, (x2, y2), r, (255, 0, 255), -1)
            cv.circle(img, (cx, cy), r, (0, 0, 255), -1)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]
        
def main():
    cap = cv.VideoCapture(0) 
    pTime = 0
    cTime = 0
    detector = handDetector()
    while True:
        isTrue,img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist)!=0:
             print(lmlist[3])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv.putText(img,str(int(fps)),(50,100),cv.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        cv.imshow('Image',img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()