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
    import time
    from socket import * #okay
    from pygame.locals import *
except ImportError as err:
    print("couldn't load module.")
    sys.exit(2)

screenW = 478 # was 850
screenH = 298 # was 670
"""calculating the size of the grid
number of blocks wide = (screenW // width of block.png) + 1
to check:
    screenW = 850
    block.png size = 10*10
    850 // 12 = 70
    70 + 1 = 71
    71 * 10  = 710 pixels
    2 blank pixels after each block except last one on the grid
    2 * 70 = 140 blank pixels
    140 + 710 = 850 = screenW
number of block tall = (screenH // height of block.png) + 1"""
diff1 = 1/10
diff2 = 1/20
diff3 = 1/30

gray = (171, 171, 171)

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
    except pygame.error():
        print('Cannot load image:', fullname)
        raise SystemExit()
    return image, image.get_rect()

class body(pygame.sprite.Sprite):

    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('block.png')[0]
        self.rect = load_png('block.png')[1]
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = "up"
        self.speed = 12

    def moveUp(self):
        self.direction = "up"
        if self.rect.top > 0:
            self.rect.y = self.rect.y - self.speed

    def moveDown(self):
        self.direction = "down"
        if self.rect.bottom < screenH:
            self.rect.y = self.rect.y + self.speed

    def moveLeft(self):
        self.direction = "left"
        if self.rect.left > 0:
            self.rect.x = self.rect.x - self.speed

    def moveRight(self):
        self.direction = "right"
        if self.rect.right < screenW:
            self.rect.x = self.rect.x + self.speed


class food(pygame.sprite.Sprite):

    def __init__(self, parts, head):
        """snake is a list of tuples where each tuple contains the center x and center y coordinates of each
        segment of the snake"""
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('food.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.centerx, self.rect.centery = self.setLocation(parts, head)
        print(self.rect.center)

    def setLocation(self, parts, head):
        center = self.findLocation()
        while center in parts or not self.inBounds(center) or center == head:
            center = self.findLocation()
        return center

    def findLocation(self):
        #randomly chooses coordinates for the food that will be on the same grid as the snake
        x = random.randint(0,screenW)
        y = random.randint(0,screenH)

        if x % 12 == 11 and y % 12 == 11: # neither x nor y are on the grid
            x = x - 6
            y = y - 6
        elif x % 12 != 11 and y % 12 == 11:# y is not on the grid
            y = y - 6
            x = self.nearest(x)
        elif x % 12 == 11 and y % 12 != 11:# x is not on the grid
            x = x - 6
            y = self.nearest(y)
        elif x % 12 != 11 and y % 12 != 11:# both x and y are on the grid
            x = self.nearest(x)
            y = self.nearest(y)

        return (x,y)

    def nearest(self, z):
        #looks forward and back 6 pixels to find the nearest center
        zz = z
        while z % 12 != 5 and z < zz + 7:
            z = z + 1

        if z % 12 == 5:
            return z

        else:
            z = zz
            while z % 12 != 5 and z > zz - 7:
                z = z - 1

            return z

    def inBounds(self, xy):
        #returns false if x and or y are beyond the edges of the screen
        x = xy[0]
        y = xy[1]

        if x > screenW or y > screenH:
            return False

        return True


def findDir(snake):
    #returns the corresponding key for the direction the snake is moving in
    if snake.direction == "up":
        return K_UP
    elif snake.direction == "down":
        return K_DOWN
    elif snake.direction == "left":
        return K_LEFT
    elif snake.direction == "right":
        return K_RIGHT

def update(snake, parts):
    """parts is a list containing the coordinates of each segment of the snake's body
       this function shifts each item in parts back one place and replaces the first item with the
       current position of the snake"""
    i = len(parts) - 1

    while i > 0:
        parts[i] = parts[i-1]
        i = i-1

    dir = snake.direction
    if dir == "up":
        x = snake.rect.centerx
        y = snake.rect.centery + 12
    elif dir == "down":
        x = snake.rect.centerx
        y = snake.rect.centery - 12
    elif dir == "left":
        y = snake.rect.centery
        x = snake.rect.centerx + 12
    elif dir == "right":
        y = snake.rect.centery
        x = snake.rect.centerx - 12

    parts[0] = (x,y)

    return parts

def genSegments(parts):
    """generates body objects with the coordinates in the list of parts"""
    segments = []
    for p in parts:
        x = p[0] - 5 #subraction is to return the index of the corner pixel instead of the center
        y = p[1] - 5
        part = body(x,y)
        segments.append(part)

    return segments

def blitBody(screen, background, body):
    # blits each segment of the snake's body
    for s in body:
        screen.blit(background, s.rect, s.rect)

def auto (snake, food):
    """a function that lets the game play itself"""
    sx= snake.rect.centerx
    sy = snake.rect.centery
    fx = food.rect.centerx
    fy = food.rect.centery

    if sy > fy and snake.direction != "down":
        return "up"
    if sy < fy and snake.direction != "up":
        return "down"
    if sx > fx and snake.direction != "right":
        return "left"
    if sx < fx and snake.direction != "left":
        return "right"

    if snake.rect.top > 0:
        return "up"
    if snake.rect.right < screenW:
        return "right"
    if snake.rect.bottom < screenH:
        return "down"
    if snake.rect.left > 0:
        return "left"




def main():
    # Initialise screen
    pygame.init()

    global screen
    global background

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
    snake.image, snake.rect = load_png('head.png')
    snakeSprite = pygame.sprite.RenderPlain(snake)

    parts = []
    f = food(parts, snake.rect.center)
    foodSprite = pygame.sprite.RenderPlain(f)

    score = 0
    font = pygame.font.Font(None, 30)
    scoreText = font.render("score: " + str(score), 1, gray)
    textpos = scoreText.get_rect()
    textpos.midbottom = background.get_rect().midbottom

    lose  = False
    # Blit everything to the screen
    screen.blit(background, (0,0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    pause = 0



    snake.rect.x = 240
    snake.rect.y = 144
    while True:

        for event in pygame.event.get():
                if event.type == QUIT:
                    return

        #lose = False #i need to test without losing

        if not lose:
            clock.tick(60)

            if event.type == KEYDOWN and event.key == K_p and pause == 1:
                pause = pause - 1
                pygame.event.pump()
                event.key = findDir(snake) #prevents the game from re-pausing itself since the most recent key in the queue will no longer be p

            if pause == 0:
                time.sleep(diff2)

                #snake.direction = auto(snake, f)#TESTING STUFF OUT ON THIS LINE
                if snake.direction == "up":
                    if snake.rect.top != 0:
                        snake.moveUp()
                    else:
                        lose = True
                elif snake.direction == "down":
                    if snake.rect.bottom != screenH:
                        snake.moveDown()
                    else:
                        lose = True
                elif snake.direction == "left":
                    if snake.rect.left != 0:
                        snake.moveLeft()
                    else:
                        lose = True
                elif snake.direction == "right":
                    if snake.rect.right != screenW:
                        snake.moveRight()
                    else:
                        lose = True

                if snake.rect.center in parts:
                    lose = True

                print(snake.rect.center + f.rect.center)
                if snake.rect.center == f.rect.center:
                    parts.append(f.rect.center)
                    #print(parts)
                    #loc = parts
                    score = score + 10
                    scoreText = font.render("score: " + str(score), 1, gray)
                    f.rect.center = f.setLocation(parts, snake.rect.center)

                if len(parts) > 0:
                    parts = update(snake, parts)
                    bodyParts = genSegments(parts)
                    bodySprites = pygame.sprite.RenderPlain([a for a in bodyParts])

                if event.type == KEYDOWN:
                    if event.key == K_UP and snake.direction != "down":
                        snake.direction = "up"
                        pygame.event.pump()
                    if event.key == K_DOWN and snake.direction != "up":
                        snake.direction = "down"
                        pygame.event.pump()
                    if event.key == K_LEFT and snake.direction != "right":
                        snake.direction = "left"
                        pygame.event.pump()
                    if event.key == K_RIGHT and snake.direction != "left":
                        snake.direction = "right"
                        pygame.event.pump()
                    if event.key == K_p:
                        pause = pause + 1
                        pygame.event.pump()
                        event.key = findDir(snake)



            screen.blit(background, (0,0))
            screen.blit(background, snake.rect, snake.rect)
            screen.blit(background, f.rect, f.rect)
            screen.blit(scoreText, textpos)
            if len(parts) > 0:
                blitBody(screen, background, bodyParts)
            snakeSprite.draw(screen)
            foodSprite.draw(screen)
            if len(parts) > 0:
                bodySprites.draw(screen)
            pygame.display.flip()

if __name__ == '__main__': main()