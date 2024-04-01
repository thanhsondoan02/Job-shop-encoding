import pygame

def alarm():
  pygame.mixer.init()
  pygame.mixer.music.load("./phonk_cristino_siuuu.mp3")
  pygame.mixer.music.play()
