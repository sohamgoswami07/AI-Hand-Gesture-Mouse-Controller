import cv2
import mediapipe as mp

class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.7, trackCon=0.7):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=mode,
            max_num_hands=maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.lmList = []
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        return img

    def findPosition(self, img, handNo=0, draw=True, showActiveOnly=False, fingersState=None):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            if handNo < len(self.results.multi_hand_landmarks):
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, cx, cy])
                    if draw and id in self.tipIds:
                        if showActiveOnly and fingersState:
                            fingerIndex = self.tipIds.index(id)
                            if fingersState[fingerIndex] == 1:
                                cv2.circle(img, (cx, cy), 12, (255, 255, 255), 2)
                        elif not showActiveOnly:
                            cv2.circle(img, (cx, cy), 12, (255, 255, 255), 2)
        return self.lmList, img

    def fingersUp(self):
        fingers = [0, 0, 0, 0, 0]
        if len(self.lmList) == 0:
            return fingers

        # Thumb
        fingers[0] = int(self.lmList[4][1] > self.lmList[3][1])  # Assume right hand

        # Fingers (index to pinky)
        for i in range(1, 5):
            fingers[i] = int(self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2])

        return fingers
