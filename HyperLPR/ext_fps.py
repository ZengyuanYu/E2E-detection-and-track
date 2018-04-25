#-*- coding utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt


cap=cv2.VideoCapture('./images_rec/car_track.mp4')
count = 5
while(True):
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    cv2.imwrite("./images_rec/%d.jpg" % count, gray)
    count = count + 1
    cv2.imshow('frame',gray)

    if cv2.waitKey(1)&0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWidows()