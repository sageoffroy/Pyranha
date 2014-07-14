#!/usr/bin/env python2

#import pygame
#import time
import pyglet
def playBeep():
    #pygame.init()
    #pygame.mixer.music.load('sound/BEEP1.WAV')
    #pygame.mixer.music.play()
    #time.sleep(0.001)
    sound = pyglet.resource.media('sound/BEEP1.WAV')
    sound.play()
    
def playDing():
    sound = pyglet.resource.media('sound/DING.wav')
    sound.play()