#snake game
#Matthew Kennedy
#mkennedm@bu.edu
#MKennedyMSM@gmail.com
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
number of blocks wide = (screenW // (width of block.png + number of horizontal pixels between blocks)) + 1
to check:
    screenW = 478
    block.png size = 10*10
    width of block + pixels between adjacent blocks = 12
    478 // 12 = 39
    39 + 1 = 40
    40 * 10  = 400 pixels
    2 blank pixels after each block except last one on the grid
    2 * 39 = 78 blank pixels
    78 + 400 = 478 = screenW
number of block tall = (screenH // (height of block.png + number of vertical pixels between blocks)) + 1

width = 40 blocks
height = 25 blocks
totals blocks in grid = 25 * 40 = 1000"""

gray = (171, 171, 171)
black = (41, 41, 41)
red = (205, 0, 0)


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
        self.direction = "left"
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

    def moveGiven(self, dir):
        if dir == "up":
            self.moveUp()
        elif dir == "down":
            self.moveDown()
        elif dir == "left":
            self.moveLeft()
        elif dir == "right":
            self.moveRight()


class food(pygame.sprite.Sprite):

    def __init__(self, parts, head):
        """snake is a list of tuples where each tuple contains the center x and center y coordinates of each
        segment of the snake"""
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('food.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.centerx, self.rect.centery = self.setLocation(parts, head)

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

    if len(parts) > 0:
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

def auto (snake, food, parts):
    """a function that lets the game play itself"""
    sx= snake.rect.centerx
    sy = snake.rect.centery
    fx = food.rect.centerx
    fy = food.rect.centery

    if (sy > fy and snake.direction != "down" and snake.rect.top > 0
            and (snake.rect.centerx, snake.rect.centery - 12) not in parts):
        return "up"
    if (sy < fy and snake.direction != "up" and snake.rect.bottom < screenH
            and (snake.rect.centerx, snake.rect.centery + 12) not in parts):
        return "down"
    if (sx > fx and snake.direction != "right" and snake.rect.left > 0
            and (snake.rect.centerx - 12, snake.rect.centery) not in parts):
        return "left"
    if (sx < fx and snake.direction != "left" and snake.rect.right < screenW
            and (snake.rect.centerx + 12, snake.rect.centery) not in parts):
        return "right"

    if snake.rect.top > 0 and (snake.rect.centerx, snake.rect.centery - 12) not in parts:
        print("second up")
        return "up"
    if snake.rect.right < screenW and (snake.rect.centerx + 12, snake.rect.centery) not in parts:
        print("second right")
        return "right"
    if snake.rect.bottom < screenH and (snake.rect.centerx, snake.rect.centery + 12) not in parts:
        print("second down")
        return "down"
    if snake.rect.left > 0 and (snake.rect.centerx - 12, snake.rect.centery) not in parts:
        print("second left")
        return "left"

    print("all tests failed")
    return snake.direction

def advancedAuto (snake, food, parts):
    """a function that lets the game play itself"""
    sx= snake.rect.centerx
    sy = snake.rect.centery
    fx = food.rect.centerx
    fy = food.rect.centery

    if (sy > fy and snake.direction != "down" and snake.rect.top > 0
            and not bodyBetween(snake, parts, food, "up") and not hitBody(snake, parts, "up")):
        return "up"
    if (sy < fy and snake.direction != "up" and snake.rect.bottom < screenH
            and not bodyBetween(snake, parts, food, "down") and not hitBody(snake, parts, "down")):
        return "down"
    if (sx > fx and snake.direction != "right" and snake.rect.left > 0
            and not bodyBetween(snake, parts, food, "left") and not hitBody(snake, parts, "left")):
        return "left"
    if (sx < fx and snake.direction != "left" and snake.rect.right < screenW
            and not bodyBetween(snake, parts, food, "right") and not hitBody(snake, parts, "right")):
        return "right"

    #consider removing the top block of ifs try incorporating distance into lookAhead
    #print("all tests failed")
    return lookAhead(snake, parts, food)

def lookAhead(head, body, food):
    """determines the best possible move by looking 3 spaces ahead in each of the three possible directions"""
    if head.direction == "up":
        up = threeAhead(head, body, food, "up")
        left = threeAhead(head, body, food, "left")
        right = threeAhead(head, body, food, "right")
        best = max(up,left,right)
        if best == up:
            return "up"
        elif best == left:
            return "left"
        elif best == right:
            return "right"

    elif head.direction == "down":
        down = threeAhead(head, body, food, "down")
        left = threeAhead(head, body, food, "left")
        right = threeAhead(head, body, food, "right")
        best = max(down,left,right)
        if best == down:
            return "down"
        elif best == left:
            return "left"
        elif best == right:
            return "right"

    elif head.direction == "left":
        down = threeAhead(head, body, food, "down")
        left = threeAhead(head, body, food, "left")
        up = threeAhead(head, body, food, "up")
        best = max(down,left,up)
        if best == down:
            return "down"
        elif best == left:
            return "left"
        elif best == up:
            return "up"

    elif head.direction == "right":
        down = threeAhead(head, body, food, "down")
        right = threeAhead(head, body, food, "right")
        up = threeAhead(head, body, food, "up")
        best = max(down,right,up)
        if best == down:
            return "down"
        elif best == right:
            return "right"
        elif best == up:
            return "up"


def threeAhead(head, body, food, dir):
    """looks three places ahead in the given direction and return a grade based on how good of a move it is"""
    i = 0
    max  = 8 #change back to 5 if things break
    grade = 0
    hx = head.rect.centerx
    hy = head.rect.centery

    if dir == "up":
        while i < max:
            pos  = (hx, hy - (12*i))
            if pos not in body and hy - (12*i) > 0:
                if pos != food.rect.center:
                    grade = grade + 1
                elif pos == food.rect.center:
                    grade = grade + max + 2
                i = i + 1
            else:
                grade = grade - 2
                i = max
        if (dist(pos, food) < distance(head, food)):
            grade = grade + 1
        #print("threeAhead up grade: " + str(grade))
    elif dir == "down":
            while i < max:
                pos = (hx, hy + (12*i))
                if pos not in body and hy + (12*i) < screenH:
                    if pos != food.rect.center:
                        grade = grade + 1
                    elif food.rect.center == pos:
                        grade = grade + max + 2
                    i = i + 1
                else:
                    grade = grade - 2
                    i = max
            if (dist(pos, food) < distance(head, food)):
                grade = grade + 1
            #print("threeAhead down grade: " + str(grade))
    elif dir == "left":
            while i < max:
                pos = (hx - (12*i), hy)
                if pos not in body and hx - (12*i) > 0:
                    if pos != food.rect.center:
                        grade = grade + 1
                    elif food.rect.center == pos:
                        grade = grade + max + 2
                    i = i + 1
                else:
                    grade = grade - 2
                    i = max
            if (dist(pos, food) < distance(head, food)):
                grade = grade + 1
            #print("threeAhead left grade: " + str(grade))
    elif dir == "right":
            while i < max:
                pos = (hx + (12*i), hy)
                if pos not in body and hx + (12*i) < screenW:
                    if pos != food.rect.center:
                        grade = grade + 1
                    elif food.rect.center == pos:
                        grade = grade + max + 2
                    i = i + 1
                else:
                    grade = grade - 2 #change these back to 2 if things break
                    i = max
            if (dist(pos, food) < distance(head, food)):
                grade = grade + 1
            #print("threeAhead right grade: " + str(grade))

    return grade




def bodyBetween(head, body, food, dir):
    """returns true if part of the bdy is between the head of the snake and the food based on direction"""
    hx = head.rect.centerx
    hy = head.rect.centery
    fx = food.rect.centerx
    fy = food.rect.centery

    if dir == "up":
        for part in body:
            if part[1] < hy and part[1] > fy and part[0] == hx:
                return True
    elif dir == "down":
        for part in body:
            if part[1] > hy and part[1] < fy and part[0] == hx:
                return True
    elif dir == "left":
        for part in body:
            if part[0] < hx and part[0] > fx and part[1] == hy:
                return True
    elif dir == "right":
        for part in body:
            if part[0] > hx and part[0] < fx and part[1] == hy:
                return True

    return False

def hitBody(head, body, dir):
    """returns true if moving in the given direction would cause the snake to hit itself"""
    hx = head.rect.centerx
    hy = head.rect.centery

    if dir == "up":
        for part in body:
            if part[0] == hx and part[1] == hy - 12:
                #print("hitBody " + dir)
                return True
    elif dir == "down":
        for part in body:
            if part[0] == hx and part[1] == hy + 12:
                #print("hitBody " + dir)
                return True
    elif dir == "left":
        for part in body:
            if part[1] == hy and part[0] == hx - 12:
                #print("hitBody " + dir)
                return True
    elif dir == "right":
        for part in body:
            if part[1] == hy and part[0] == hx + 12:
                #print("hitBody " + dir)
                return True

    return False


def chooseMove(head, body, food):
    """uses a game tree for the AI to choose the best direction to go in"""
    max = -100
    oldBody = body
    oldHead = head.rect.center
    best = ""
    dirs = getDirs(head.direction)
    print("dirs: " + str(dirs))


    for dir in dirs:
        if not (badDir(dir, head, body)):
            print("badDir returns " + str(badDir(dir, head, body)) + " for " + dir)
            print("chooseMove: " + dir)
            print(head.rect.center)
            head.moveGiven(dir)
            body = update(head, body)
            val = tree(head, body, food, 1)
            if val >= max:
                best = dir
                max = val
            head.rect.center = oldHead
            body = oldBody
            print("just reached the branches for " + dir)
    print("max = " + str(max))
    return best

def badDir(dir, head, body):
    #return true if moving in the given direction will lose the game

    if ((dir == "up" and head.rect.y - 12 < 0) or (dir == "left" and head.rect.left - 12 < 0) or
        (dir == "right" and head.rect.right + 12 > screenW) or (dir == "down" and head.rect.bottom + 12 > screenH)):
        print("badDir " + dir)
        return True

    return False

def bestDir(head, food, dir):
    oldHead = head.rect.center
    head.moveGiven(dir)
    if head.rect.center == food.rect.center:
        head.rect.center = oldHead
        return True
    else:
        return False

def availableSpaces(head, body):
    """rates the quality of a move based on how many available spaces there are for the next move"""
    score = 0
    rect = head.rect

    if head.direction == "up":
        if rect.centery - 12 > 0 and ((rect.centerx, rect.centery - 12) not in body):
            score = score + 1
        if rect.centerx - 12 > 0 and ((rect.centerx - 12, rect.centery) not in body):
            score = score + 1
        if rect.centerx + 12 < screenW and ((rect.centerx + 12, rect.centery) not in body):
            score = score + 1
    elif head.direction == "down":
        if (rect.centery + 12 < screenH) and ((rect.centerx, rect.centery + 12) not in body):
            score = score + 1
        if rect.centerx - 12 > 0 and ((rect.centerx - 12, rect.centery) not in body):
            score = score + 1
        if rect.centerx + 12 < screenW and ((rect.centerx + 12, rect.centery) not in body):
            score = score + 1
    elif head.direction == "left":
        if rect.centerx - 12 > 0 and ((rect.centerx - 12, rect.centery) not in body):
            score = score + 1
        if rect.centery - 12 > 0 and ((rect.centerx, rect.centery - 12) not in body):
            score = score + 1
        if rect.centery + 12 < screenH and ((rect.centerx, rect.centery + 12) not in body):
            score = score + 1
    elif head.direction == "right":
        if rect.centerx + 12 < screenW and ((rect.centerx + 12, rect.centery) not in body):
            score = score + 1
        if rect.centery - 12 > 0 and ((rect.centerx, rect.centery - 12) not in body):
            score = score + 1
        if rect.centery + 12 < screenH and ((rect.centerx, rect.centery + 12) in body):
            score = score + 1

    return score


def tree(head, body, food, depth):
    # traverses down the tree of potential moves and calls eval when it reaches a leaf

    if (depth == 3 or head.rect.center in body):
        print("               tree level 3" + " " + head.direction)
        return eval(head, food, body, depth)

    val = -1000
    oldBody = body
    oldHead = head.rect.center
    dirs = getDirs(head.direction)

    for dir in dirs:
        if not (badDir(dir, head, body) or hitBody(head, body, dir)):
            if depth == 1:
                print("     tree level 1" + " " + dir)
            if depth == 2:
                print("          tree level 2" + " " + dir)
            head.moveGiven(dir)
            update(head, body)
            val = max(val, tree(head, body, food, depth + 1))
            head.rect.center = oldHead
            body = oldBody

    return val


def getDirs(dir):
    "returns a list of direction not including the opposite of the one given"
    if dir == "up":
        return ["up","left","right"]
    elif dir == "down":
        return ["down","left","right"]
    elif dir == "left":
        return ["left","up","down"]
    elif dir == "right":
        return ["right", "up", "down"]

def distance(head, food):
    x1 = head.rect.centerx
    x2 = food.rect.centerx
    y1 = head.rect.centery
    y2 = food.rect.centery

    #print("head x = " + str(x1) + " y = " + str(y1) + " food x = " + str(x2) + " y = " + str(y2))
    return math.sqrt(pow((x2-x1),2) + pow((y2-y1),2))

def dist(pos, food):
    """finds the distance between two points"""
    x1 = pos[0]
    x2 = food.rect.centerx
    y1 = pos[1]
    y2 = food.rect.centery
    distance = math.sqrt(pow((x2-x1),2) + pow((y2-y1),2))

    #print("head x = " + str(x1) + " y = " + str(y1) + " food x = " + str(x2) + " y = " + str(y2) + " distance = " + str(distance))
    return distance

def eval(head, food, body, depth):
    #evaluates how good a move is
    dir = head.direction
    score = 0
    currentPos = head.rect.center

    if dir == "left":
        dirs = ["left", "up", "down"]
    elif dir == "right":
        dirs = ["right", "up", "down"]
    elif dir == "up":
        dirs = ["up", "left", "right"]
    elif dir == "down":
        dirs = ["down", "left", "right"]

    for d in dirs:
        head.moveGiven(d)
        #print("evaluating " + d)
        #consider giving negative points for bad moves if current method proves ineffective
        if head.rect.center not in body and head.rect.center != currentPos:
            score = score + 1
        if head.rect.center == currentPos:
            score = score - 1
        if head.rect.center in body:
            score = score - 1
        if dist(head.rect.center, food) < dist(currentPos, food):
            score = score + 7
        head.rect.center = currentPos
        if head.rect.center == food.rect.center:
            score = score + 10

        score = score + availableSpaces(head, body)

        head.rect.center = currentPos
        if depth == 1:
            print("     evaluating " + d + " score = " + str(score))
        if depth == 2:
            print("          evaluating " + d + " score = " + str(score))
        if depth == 3:
            print("               evaluating " + d + " score = " + str(score))

    return score



def testFood(head, food, parts):
    """needed this to make sure food was not appearing inside the snake's body"""
    if head.direction != "right" and head.rect.x != 0:
        return "left"
    if head.direction != "left" and head.rect.right != screenW:
        return "right"
    if (head.direction == "left" and head.rect.x == 0) or (head.direction == "right" and head.rect.right == screenW):
        return "up"
    else:
        return advancedAuto(head, food, parts)

def runGame(difficulty):
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption('Snake')

    if difficulty == "easy":
        diff = 10
    elif difficulty == "medium":
        diff = 20
    elif difficulty == "hard" or difficulty == "demo":
        diff = 30


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
    font = pygame.font.SysFont('vrindi', 30, False, False)
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

    blitOnce = 0

    while True:

        for event in pygame.event.get():
                if event.type == QUIT:
                    return None

        #lose = False #i need to test without losing

        if not lose:
            clock.tick(60)

            if event.type == KEYDOWN and event.key == K_p and pause == 1:
                pause = pause - 1
                pygame.event.pump()
                event.key = findDir(snake) #prevents the game from re-pausing itself since the most recent key in the queue will no longer be p

            if pause == 0:
                time.sleep(1/diff)

                if difficulty == "demo":
                    #snake.direction = auto(snake, f, parts)
                    snake.direction = advancedAuto(snake, f, parts)
                    #snake.direction = testFood(snake,f, parts)
                    #snake.direction = chooseMove(snake, parts, f)
                    #print("|||||||||||||||||||||||||||||||||||| " + snake.direction + " |||||||||||||||||||||||||||||")
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

                #print(snake.rect.center + f.rect.center)
                if snake.rect.center == f.rect.center:
                    parts.append(f.rect.center)
                    #print(parts)
                    score = score + 10
                    scoreText = font.render("score: " + str(score), 1, gray)
                    f.rect.center = f.setLocation(parts, snake.rect.center)

                if len(parts) > 0 and not lose:
                    parts = update(snake, parts)
                    bodyParts = genSegments(parts)
                    bodySprites = pygame.sprite.RenderPlain([a for a in bodyParts])

                if event.type == KEYDOWN:
                    if (event.key == K_UP or event.key == K_w) and snake.direction != "down":
                        snake.direction = "up"
                        pygame.event.pump()
                    if (event.key == K_DOWN or event.key == K_s) and snake.direction != "up":
                        snake.direction = "down"
                        pygame.event.pump()
                    if (event.key == K_LEFT or event.key == K_a) and snake.direction != "right":
                        snake.direction = "left"
                        pygame.event.pump()
                    if (event.key == K_RIGHT or event.key == K_d) and snake.direction != "left":
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

        if lose:
            """text that will appear on the screen superimposed over the game that just finished"""
            gameFont = pygame.font.SysFont('vrindi', 50, False, False)
            gameOver = gameFont.render("Game Over", 1, black)

            instrucFont = pygame.font.SysFont('vrindi', 20, False, False)
            restart = instrucFont.render("Press the space bar to restart", 1, black)
            mainMen = instrucFont.render("Click here to return to main menu", 1, black)
            mainMenRed = instrucFont.render("Click here to return to main menu", 1, red)

            gameOverRect = gameOver.get_rect()
            restartRect = restart.get_rect()
            mainRect = mainMen.get_rect()
            mainRedRect = mainMenRed.get_rect()

            gameOverRect.midbottom = background.get_rect().center
            restartRect.midtop = gameOverRect.midbottom
            mainRect.midtop = restartRect.midbottom
            mainRect.y = mainRect.y + 15
            gameOverRect.y = gameOverRect.y - 15
            mainRedRect.center = mainRect.center

            rects = [(gameOver, gameOverRect), (restart, restartRect), (mainMen, mainRect)]

            if blitOnce == 0:
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
                blitRects(screen, rects)
                pygame.display.flip()
                blitOnce = 1

            if event.type == MOUSEMOTION:
                    screen.blit(background,mainRect)
                    screen.blit(scoreText, textpos)
                    snakeSprite.draw(screen)
                    foodSprite.draw(screen)
                    if len(parts) > 0:
                        bodySprites.draw(screen)

                    if mainRect.collidepoint(event.pos):
                        screen.blit(mainMenRed, mainRedRect)
                    else:
                        screen.blit(mainMen, mainRect)

                    pygame.display.flip()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if mainRect.collidepoint(event.pos):
                        return "menu"

            if event.type == KEYDOWN:
                    if (event.key == K_SPACE):
                        return difficulty



def startMenu():
    instrucFont = pygame.font.SysFont('vrindi', 20, False, False)
    control = instrucFont.render("Use arrow keys or w,a,s, and d keys for movement", 1, black)
    pause = instrucFont.render("Press P to pause the game", 1, black)

    gameFont = pygame.font.SysFont('vrindi', 30, False, False)
    diff = gameFont.render("Choose difficulty", 1, black)
    easy = gameFont.render("Easy", 1, black)
    easyRed = gameFont.render("Easy", 1, red)
    med = gameFont.render("Medium", 1, black)
    medRed = gameFont.render("Medium", 1, red)
    hard = gameFont.render("Hard", 1, black)
    hardRed = gameFont.render("Hard", 1, red)
    demo = gameFont.render("Demo", 1, black)
    demoRed = gameFont.render("Demo", 1, red)


    titleFont = pygame.font.SysFont('vrindi', 50, False, False)
    title = titleFont.render("Snake", 1, black)

    controlRect = control.get_rect()
    pauseRect = pause.get_rect()
    diffRect = diff.get_rect()
    easyRect = easy.get_rect()
    easyRedRect =  easyRed.get_rect()
    medRect = med.get_rect()
    medRedRect = medRed.get_rect()
    hardRect = hard.get_rect()
    hardRedRect = hardRed.get_rect()
    titleRect = title.get_rect()
    demoRect = demo.get_rect()
    demoRedRect = demoRed.get_rect()

    backRect = background.get_rect()

    diffRect.midbottom = backRect.center
    diffRect.y = diffRect.y - 40
    easyRect.midtop = diffRect.midbottom
    medRect.midtop = easyRect.midbottom
    hardRect.midtop = medRect.midbottom
    controlRect.midtop = hardRect.midbottom
    controlRect.y = controlRect.y + 15
    pauseRect.midtop = controlRect.midbottom
    titleRect.midbottom = diffRect.midtop
    demoRect.midtop = pauseRect.midbottom
    demoRect.y = demoRect.y + 10

    easyRedRect.center = easyRect.center
    medRedRect.center = medRect.center
    hardRedRect.center = hardRect.center
    demoRedRect.center = demoRect.center

    titleRect.y = titleRect.y - 15

    blackRects = [(control, controlRect), (pause, pauseRect), (diff, diffRect), (easy, easyRect),
                 (med, medRect), (hard, hardRect), (title, titleRect), (demo, demoRect)]

    screen.blit(background, (0,0))
    for rect in blackRects:
            screen.blit(rect[0], rect[1])

    while True:
        for event in pygame.event.get():
                if event.type == QUIT:
                    return None

                if event.type == MOUSEMOTION:
                    if easyRect.collidepoint(event.pos):
                        screen.blit(background, (0,0))
                        blitRects(screen, blackRects)
                        screen.blit(easyRed, easyRedRect)
                        #pygame.display.flip()
                    elif medRect.collidepoint(event.pos):
                        screen.blit(background, (0,0))
                        blitRects(screen, blackRects)
                        screen.blit(medRed, medRedRect)
                    elif hardRect.collidepoint(event.pos):
                        screen.blit(background, (0,0))
                        blitRects(screen, blackRects)
                        screen.blit(hardRed, hardRedRect)
                    elif demoRect.collidepoint(event.pos):
                        screen.blit(background, (0,0))
                        blitRects(screen, blackRects)
                        screen.blit(demoRed, demoRedRect)
                    else:
                        screen.blit(background, (0,0))
                        blitRects(screen, blackRects)

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if easyRect.collidepoint(event.pos):
                        return "easy"
                    if medRect.collidepoint(event.pos):
                        return "medium"
                    if hardRect.collidepoint(event.pos):
                        return "hard"
                    if demoRect.collidepoint(event.pos):
                        return "demo"

        pygame.display.flip()


def blitRects(screen, rects):
    """ blits the text from each font to its rect
    made this into its own function since the steps are repeated several times in startMenu()"""
    for rect in rects:
        screen.blit(rect[0], rect[1])



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

    finish = "menu"

    while finish != None:
        for event in pygame.event.get():
            if event.type == QUIT:
                finish = None
        if finish == "menu":
            diff = startMenu()
            if diff != None:
                finish = runGame(diff)
            else:
                finish = None
        elif finish == "easy" or finish == "medium" or finish == "hard" or finish == "demo":
            finish = runGame(finish)
        else:
            finish = None




if __name__ == '__main__': main()