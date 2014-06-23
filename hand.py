#!/usr/bin/env python2

"""
OpenCV example. Show webcam image and detect 
.
"""

import cv2
from ruido import *
TRAINSET = "cascade/cascade.xml"
DOWNSCALE = 4

webcam = cv2.VideoCapture(0)
cv2.namedWindow("preview")
classifier = cv2.CascadeClassifier(TRAINSET)


if webcam.isOpened(): # try to get the first frame
    rval, frame = webcam.read()
    
else:
    rval = False

while rval:

    # detect faces and draw bounding boxes
    minisize = (frame.shape[1]/DOWNSCALE,frame.shape[0]/DOWNSCALE)
    miniframe = cv2.resize(frame, minisize)
    hands = classifier.detectMultiScale(miniframe)
    for f in hands:
        print ("mano")
        playBeep()
        x, y, w, h = [ v*DOWNSCALE for v in f ]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))

    #cv2.flip(frame,1,frame)#para espejar la imagen
    #cv2.putText(frame, "ESC para salir", (5, 25),
    #            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
    #cv2.imshow("Vista previa", frame)

    # get next frame
    rval, frame = webcam.read()

    #key = cv2.waitKey(20)
    #if key in [27, ord('Q'), ord('q')]: # exit on ESC
    #    break

