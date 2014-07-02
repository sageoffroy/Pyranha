#!/usr/bin/env python2

import pygame
import time

def playBeep():
    pygame.init()
    pygame.mixer.music.load('sound/BEEP1.WAV')
    pygame.mixer.music.play()
    time.sleep(0.001)