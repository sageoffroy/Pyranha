#!/usr/bin/env python2


import time
#import pyglet
import pygame

def playBeep():
    pygame.mixer.init()
    time.sleep(0.001)
    #sound = pyglet.resource.media('sound/BEEP1.WAV')
    sound = pygame.mixer.Sound('sound/BEEP1.WAV')
    sound.play()
    
def playDing():
    pygame.mixer.init()
    sound = pygame.mixer.Sound('sound/DING.wav')
    #sound = pyglet.resource.media('sound/DING.wav')
    sound.play()
    #pygame.mixer.stop()
