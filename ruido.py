#!/usr/bin/env python2


import time
import pyglet

def playBeep():
    time.sleep(0.001)
    sound = pyglet.resource.media('sound/BEEP1.WAV')
    sound.play()
    
def playDing():
    sound = pyglet.resource.media('sound/DING.wav')
    sound.play()

