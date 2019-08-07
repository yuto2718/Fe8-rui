import cv2
import numpy as np
import matplotlib.pyplot as plt


mousthpath = ''

kernel = np.array([[1, 1,  1],
                   [1, -8, 1],
                   [1, 1,  1]])

cap = cv2.VideoCapture(1)

pframe = None

while True:
    ret,frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gaussian = cv2.GaussianBlur(gray, (3,3), 0)
    gray = cv2.medianBlur(gaussian,7)


    if pframe is None:
        pframe  = gray.copy().astype('float')
        continue

    cv2.accumulateWeighted(gray, pframe, 0.7)
    deltaFrame = cv2.absdiff(gray, cv2.convertScaleAbs(pframe))

    ref,bin = cv2.threshold(deltaFrame, 3, 255, cv2.THRESH_BINARY)

    image, contours, hierarchy = cv2.findContours(bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    target = contours[0]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if max_area < area and area < 10000 and area > 800:
            max_area = area;
            target = cnt

    if max_area <= 800:
        areaFrame = frame
        cv2.putText(areaFrame, 'not detected', (0,50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255,0), 3, cv2.LINE_AA)
    else:
        x,y,w,h = cv2.boundingRect(target)
        areaFrame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow('move', frame)

    k = cv2.waitKey(1)
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
        quit()

cap.release()
cv2.destroyAllWindows()
