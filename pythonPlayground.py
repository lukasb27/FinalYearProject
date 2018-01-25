# import pygame
# import time
#
# pygame.init()
# pygame.mixer.music.load('Applause.mp3')
# print('play')
# pygame.mixer.music.play(-1, 0.0)
# print('sleep')
# time.sleep(2)
# print('stop')
# pygame.mixer.music.pause()

from server import server
from client import client

ip = server()

print(ip)


