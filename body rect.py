#snake game
#Matthew Kennedy
#August 2014
__author__ = 'Matthew'

VERSION = "0.4"

try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import * #okay
    from pygame.locals import *
except ImportError as err:
    print("couldn't load module.")
    sys.exit(2)

redX=5
redY=125
greenX=175
greenY=125
blueX=275
blueY=125

screenW = 830
screenH = 650

def load_png(name):
    """ Load image and return image object """
    #fullname = os.path.join("data", name)
    fullname = name
    try :
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error(message):
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image, image.get_rect()

class body(pygame.Rect):

    color = (100,10,10)

    def __init__(self, x , y):
        self.rect = (x,y), (50,50)
        #self.rect = load_png('block.png')
        self.width = 50
        self.height = 50
        self.direction = "right"
        self.speed = 60



    def moveUp(self):
        self.direction = "up"
        if self.top > 0:
            self.y = self.y - self.speed

    def moveDown(self):
        self.direction = "down"
        if self.bottom < screenH:
            self.y = self.y + self.speed

    def moveLeft(self):
        self.direction = "left"
        if self.left > 0:
            self.x = self.x - self.speed

    def moveRight(self):
        self.direction = "right"
        if self.right < screenW:
            self.x = self.x + self.speed

def move(rect):
    rect.x = rect.x+5

def wrap(rect):
    rect.x = 0

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption('Snake')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))



    #took following code from http://nullege.com/codes/show/src@p@y@Pygame-Examples-For-Learning-HEAD@colorPlay.py/96/pygame.draw.rect
    #red = pygame.draw.rect(background,(255,0,0),((redX,redY),(50,50)),0)
    #code above was copied from http://nullege.com/codes/show/src@p@y@Pygame-Examples-For-Learning-HEAD@colorPlay.py/96/pygame.draw.rect

    snake = body(0,0)
    #pygame.draw.rect(background, (250, 250, 250), ((0,0),(50,50)), 0)

    # Blit everything to the screen
    pygame.draw.rect(background, snake.color, snake.rect, 0)
    screen.blit(background, (0,0))
    screen.blit(background, snake)
    pygame.display.flip()

    #screen.blit(background, snake)
    #screen.blit(background, red)
    while True:
        pygame.time.Clock().tick(3)
        old = snake
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        """if red.x + 50 < 800:
            move(red)
        else:
            wrap(red)"""
        if event.type == KEYDOWN:
            if event.key == K_UP:
                snake.moveUp()
            if event.key == K_DOWN:
                snake.moveDown()
            if event.key == K_LEFT:
                snake.moveLeft()
            if event.key == K_RIGHT:
                snake.moveRight()

        screen.blit(background, (0,0))
        screen.blit(background, snake)
        #screen.blit(background, red)
        pygame.display.flip()

if __name__ == '__main__': main()