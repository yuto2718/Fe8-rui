import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

cascadePathM = '/home/yuto/Documents/play/senmonten/mouth.xml'

size = [640,480]
fps = 5

cap = cv2.VideoCapture(0)
cap.set(3, size[0])
cap.set(4, size[1])
cap.set(5, fps)

cascadeMouth = cv2.CascadeClassifier(cascadePathM)

mouth = []
name =[]

while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mouthCordiante = cascadeMouth.detectMultiScale(gray, scaleFactor = 2, minNeighbors = 8, minSize = (10,10), maxSize = (200,200))

    if len(mouthCordiante) >0:
        for rect in mouthCordiante:
            mouth.append(frame[rect[0]:rect[0]+rect[2], rect[1]:rect[1]+rect[3]])
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]),(255,255,255),thickness=2)


    cv2.imshow("mouth", frame)

    k = cv2.waitKey(1)&0xff
    if k == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        quit()
