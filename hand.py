import cv2
from ruido import *

class Hand:
    
    def __init__(self):
        self.TRAINSET = "cascade/cascade.xml"
        self.DOWNSCALE = 4
        #self.webcam = cv2.VideoCapture(0)
        #cv2.namedWindow("preview")
        self.classifier = cv2.CascadeClassifier(self.TRAINSET)

    def detectHand(self):
        self.webcam = cv2.VideoCapture(0)
        if self.webcam.isOpened(): # try to get the first frame
            rval, frame = self.webcam.read()
        else:
            rval = False
            
        while rval:
	    minisize = (frame.shape[1]/self.DOWNSCALE,frame.shape[0]/self.DOWNSCALE)
	    miniframe = cv2.resize(frame, minisize)
	    hands = self.classifier.detectMultiScale(miniframe)
	    for f in hands:
		print ("mano")
		playBeep()
		x, y, w, h = [ v*self.DOWNSCALE for v in f ]
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255))
		print ("SALE TAAAb")
		self.webcam.release()
		return 1
	    rval, frame = self.webcam.read()
	    
	self.webcam.release()
	return -1

    def start(self):
        return self.detectHand()