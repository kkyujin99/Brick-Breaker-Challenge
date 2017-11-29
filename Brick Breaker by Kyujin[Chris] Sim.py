'''

@AUTHOR: Chris Sim

'''

import pygame
import math
import random

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()


BLACK = [ 0, 0, 0]
WHITE = [255 ,255 ,255]
BLUE = [ 0, 0 ,255]
FIREBRICK = [178,  34,  34]
THISTLE = [216, 191, 216]
PURPLE = [160,  32, 240]
PINK = [255, 192, 203]
ORANGE = [255, 165,   0]
YELLOW = [255, 255,   0]
NAVY = [   0,   0,   128]
ROYALPURPLE = [120,  81, 169]
ROYALBLUE = [ 65, 105, 225]
BEIGE = [245, 245, 220]

# size of breakout blocks
block_width = 25
block_height = 15
 
# play background music

pygame.mixer.music.load("dreamcomestrue.mp3")
pygame.mixer.music.set_volume(0.9)
pygame.mixer.music.play(-1)


class Block(pygame.sprite.Sprite):
 
    def __init__(self, colour, x, y):
        # constructor method
        super().__init__()
        # create an image of the block, and fill it with a colour
        self.image = pygame.Surface([block_width, block_height])

##        self.image.fill(colour)

        self.image = pygame.image.load("Brick.gif").convert()
        # fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
        # update position of object by setting rect.x and rect.y
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    speed = 9.0
    x = 0.0
    y = 180.0
    # direction of ball (in degrees)
    direction = 200
    width = 10
    height = 10
    lives = 3
    # constructor. Pass in the colour of the block, and its x and y position
    def __init__(self):
        # call the parent class (Sprite) constructor
        super().__init__()
        # create the image of the ball
        self.image = pygame.Surface([self.width, self.height])
        # colour the ball
        self.image.fill(WHITE)
        # get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()
        # get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

    def bounce(self, diff):
        # bounce off a horizontal surface (not a vertical one)
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        # sine and cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)
 
        # change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        # move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
 
        # do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
 
        # do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
 
        # do we bounce of the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        ### do we hit bottom of the screen?
        if self.y > 600:
            self.bounce(0)
            self.y = 600
            self.lives -= 1
            print(self.lives)
        return self.lives
 
class Paddle(pygame.sprite.Sprite):
 
    def __init__(self):
        # call parent constructor
        super().__init__()
 
        self.width = 80
        self.height = 15
##        self.image = pygame.Surface([self.width, self.height])
##        self.image.fill((WHITE))

        self.image = pygame.image.load("Paddle.GIF").convert()
        
        # make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.x = 0
        self.rect.y = self.screenheight-self.height
 
    def update(self):
        pos = pygame.mouse.get_pos()
        # set the left side of the paddle bar to mouse position
        self.rect.x = pos[0]
        # make sure we don't push the paddle off the right side of the screen
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width
    
pygame.init()

size = (800,600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Brick Breaker Challenge")

# define font used (size 40)
font = pygame.font.SysFont('Agency FB', 40)

# make mouse disappear when over window
pygame.mouse.set_visible(0)

# create surface to draw on
background = pygame.Surface(screen.get_size())
 
# create sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
 
# create paddle object
paddle = Paddle()
allsprites.add(paddle)
 
# create ball object
ball = Ball()
allsprites.add(ball)
balls.add(ball)
 
# top of the block (y position)
top = 80
 
# number of blocks to create
blockcount = 32

# ---- Create 5 rows of 32 blocks ----
for row in range(5):
    for column in range(0, blockcount):
        # create a block (colour,x,y)
        block = Block(ROYALPURPLE, column * (block_width + 2) + 1, top)
        blocks.add(block)
        allsprites.add(block)
    # move top of the next row down
    top += block_height + 2

# loop until user clicks close
lives = 3                                

# used to manage how fast screen updates
clock = pygame.time.Clock()

# set score to 0
score = 0

fspeed = 0

# ---- Main program loop ----
while lives > 0:
    
    # ---- Main event loop ----                        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       
            lives = 0                     

    # ---- Game logic goes here ----


    # ---- Screen-clearing code goes here ----

    # don't put other drawing commands above this
    # or they will be erased with this command
    screen.fill(BLACK)

    # ---- Drawing code goes here ----

    # update the ball and paddle position if not game over
    if lives > 0:
        # update the paddle and ball positions
        paddle.update()
        lives = ball.update()
 
    if lives < 1:
        #text = font.render("Maybe Tomorrow", True, BEIGE)
        #textpos = text.get_rect(centerx=background.get_width()/2)
        #textpos.top = 300
        #screen.blit(text, textpos)

        font = pygame.font.SysFont("comicsansms", 50)
        rn = random.randrange(1,10)
        s = "The lucky number is " + str(rn)
        label = font.render(s, 0, (80,35,200))
        label.set_alpha(800)
        screen.fill((0,0,0))
        screen.blit(label, (50,120))
        pygame.display.update()
        pygame.time.wait(3000)
 
    # see if the ball hits the paddle
    if pygame.sprite.spritecollide(paddle, balls, False):
        # 'diff' lets you try to bounce the ball left or right
        # depending where on the paddle you hit it
        diff = (paddle.rect.x + paddle.width/2) - (ball.rect.x+ball.width/2)
 
        # set the ball's y position in case
        # we hit the ball on the edge of the paddle
        ball.rect.y = screen.get_height() - paddle.rect.height - ball.rect.height - 1
        ball.bounce(diff)
        fspeed += 3

    # check for collisions between the ball and the blocks
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
 
    # if we hit a block bounce the ball
    if len(deadblocks) > 0:
        ball.bounce(0)
        score += 10
 
        # game ends if all the blocks are gone
        if len(blocks) == 0:
            lives = 0
            
    # print the score
    scoreprint = "Score: " + str(score)
    text = font.render(scoreprint, 1, ROYALBLUE)
    textpos = (0, 0)
    screen.blit(text, textpos)

    # print lives
    livesprint = "Lives: " + str(lives)
    text = font.render(livesprint, 1, FIREBRICK)
    textpos = (size[0] - 100, 0)
    screen.blit(text, textpos)


    # print paddle
    screen.blit(paddle.image, paddle.rect)
    

    # draw Everything
    allsprites.draw(screen)

    # ---- Update screen ----
    pygame.display.flip()

    # ---- Limit to 405 frames per second ----
    clock.tick(min(135+fspeed,405))


    
# close window and quit
pygame.quit()
