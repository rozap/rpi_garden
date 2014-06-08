import pygame, sys
from pygame.locals import *
import pygame.camera
from time import sleep

def main():
    pygame.init()
    pygame.camera.init()

    while True:
        cam = pygame.camera.Camera("/dev/video0",(640,480))
        cam.start()
        img = cam.get_image()
        pygame.image.save(img,"static/now.jpg")
        cam.stop()
        sleep(10)

main()
