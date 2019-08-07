from numpy import *
import cv2
import pyaudio
import wave
import json
import matplotlib.pyplot as plt
from PIL import Image
import serial
import math
import sys
import string
import base64
import urllib.request
import urllib.response
import urllib.error
import urllib.parse
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

print("fe8 was born")

cascadePathM = '/home/yuto/Documents/senmonten/mouth.xml'

size = [640,480]
fps = 15

cap = cv2.VideoCapture(0)

cap.set(3, size[0])
cap.set(4, size[1])
cap.set(5, fps)

cascadeMouth = cv2.CascadeClassifier(cascadePathM)
print("open camera")

serialPath = '/dev/ttyACM0'
head = 255

tilt = 100
pan = 230

robot = serial.Serial(serialPath, 15200)
print("open serial port")



CHUNK = 1024*12
fs = 44100;

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate=fs,
                output=True,
                input=True)


c = 340
threshold = 65536/80
d = 0.3

Neutral = [148,195] #pan tilt
max = [230, 230]
min = [60, 150]

tilt = 150
pan = 150


print("oepn audio stream")
ref,frame = cap.read()
print("fe8 setup complate")
framesR = []
framesL = []
deg = 0
ppan = 0
ptilt = 0
camDeg = []
xdeg =0
ydeg =0

while(True):
    sa = 1000
    ref,frame = cap.read()
    idataOrg = stream.read(CHUNK)
    idata = frombuffer(idataOrg, dtype=int16)
    idataR = idata[0::2]
    idataL = idata[1::2]

    if mean(abs(idataR)+abs(idataL)) > threshold:
        idataR = array(idataR, dtype=double)
        idataL = array(idataL, dtype=double)
        correlated = correlate(idataR-mean(idataR),idataL-mean(idataL),"full")
        t = argmax(correlated)-CHUNK
        t = t/(fs*2)
        L = c*t;
        deg = math.degrees(arcsin(L/d))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    mouthCordiante = cascadeMouth.detectMultiScale(gray, scaleFactor = 2.6, minNeighbors = 8, minSize = (3,3), maxSize = (200,200))

    if len(mouthCordiante) >0:
        for rect in mouthCordiante:
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]),(255,255,255),thickness=2)
            camDeg.append([(45/320)*(((rect[0]+rect[2])/2)-320), (36/240*(((rect[1]+rect[3])/2)-240))])

    if (math.isnan(deg) == True):
        deg = 0

    tiisai = 1000

    if len(camDeg) > 0:
        for cdeg in camDeg:
            sa = (cdeg[0]-deg)
            if sa < tiisai:
                tiisai = sa
                xdeg = cdeg[0]+3
                ydeg = cdeg[1]+41
    else:
        pass

    ptime = -1*xdeg+130
    ttime = 1.2*ydeg+140

    pan = math.floor(ptime)
    tilt =math.floor(ttime)

    print(pan, tilt)

    if((pan != ppan)or(ptilt != tilt)):
        robot.write(head.to_bytes(1,'big'))
        robot.write(tilt.to_bytes(1,'big'))
        robot.write(pan.to_bytes(1,'big'))
        ptilt = tilt
        ppan = pan

    cv2.imshow("mouth", frame)
    camDeg = []
    k = cv2.waitKey(1)&0xff
    if k == ord('q'):
        robot.close()
        cap.release()
        cv2.destroyAllWindows()
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("fe8 is Dead")
        quit()


cap.release()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
p.terminate()
