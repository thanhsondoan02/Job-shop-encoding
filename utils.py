import pygame

def alarm():
  pygame.mixer.init()
  pygame.mixer.music.load("./alarm.mp3")
  pygame.mixer.music.play()
