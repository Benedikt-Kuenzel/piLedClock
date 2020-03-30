import time
import datetime
from neopixel import *
import argparse
import random
 
# LED strip configuration:
LED_COUNT      = 110      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 144     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


#Define Clock Matrix for easier use
#this obviously sucks but I'm too lazy to use any sort of logic instead
#from here on we can just use x/y vector to describe pixels. [0,0] is the left bottom pixel. [10,9] is the right top pixel.
CLOCKMATRIX = [ [1,2,3,4,5,6,7,8,9,10] , [20,19,18,17,16,15,14,13,12,11], [21,22,23,24,25,26,27,28,29,30], [40,39,38,37,36,35,34,33,32,31], [41,42,43,44,45,46,47,48,49,50], [60,59,58,57,56,55,54,53,52,51], [61,62,63,64,65,66,67,68,69,70], [80,79,78,77,76,75,74,73,72,71], [81,82,83,84,85,86,87,88,89,90],[100,99,98,97,96,95,94,93,92,91],[101,102,103,104,105,106,107,108,109,110]]

FRAMEBUFFER = []

SNAKE = [[3,3], [3,2], [3,1], [3,0]]#filled with test values

elongateSNAKE = False

APPLE = [7,8]

SNAKE_FWD_VEC = [0,1]#filled with test vec
BUFF_FWD_VEC = [0,1]

dead = False


def reset():
    global FRAMEBUFFER, SNAKE, elongateSNAKE, APPLE, SNAKE_FWD_VEC, BUFF_FWD_VEC, dead

    FRAMEBUFFER = []
    elongateSNAKE = False
    APPLE = [7,8]
    SNAKE_FWD_VEC = [0,1]
    BUFF_FWD_VEC = [0,1]

    SNAKE =  [[3,3], [3,2], [3,1], [3,0]]
    dead = False

def getInputVec():
    global SNAKE_FWD_VEC
    global BUFF_FWD_VEC

    f = open("/var/www/html/snakeDirection.txt", "r")
    dir = f.readline()
    
    

    if dir == "up":
        SNAKE_FWD_VEC = [0,1]
    elif dir == "down":
        SNAKE_FWD_VEC = [0,-1]
    elif dir == "left":
        SNAKE_FWD_VEC = [-1,0]
    elif dir == "right":
        SNAKE_FWD_VEC = [1,0]

def renderApple():
    FRAMEBUFFER.append([APPLE[0], APPLE[1], Color(0,0,128)])

def renderSnake():
    for i in range(0, len(SNAKE)):
        FRAMEBUFFER.append([SNAKE[i][0], SNAKE[i][1], Color(50,50,50)])
   
def appleEaten():
    if SNAKE[0] == APPLE:
        return True
    return False

def spawnApple():
    global APPLE

    APPLE = [random.randint(0,10), random.randint(0,9)]

    while appleEaten():
         APPLE = [random.randint(0,10), random.randint(0,9)]



def snakeBiteSelf():
    global SNAKE

    tempSNAKE = list(SNAKE)
    del tempSNAKE[0]

    #print("TempSnake:", tempSNAKE)
    #print("Snake:", SNAKE)

    if SNAKE[0] in tempSNAKE:
        return True

    return False



def moveSnake():
    global elongateSNAKE 
    global SNAKE
    global BUFF_FWD_VEC
    global SNAKE_FWD_VEC

    tempLastSnakePart = SNAKE[len(SNAKE) - 1]

    #move snake body
    for i in range(len(SNAKE) -1, 0, -1):
        SNAKE[i] = SNAKE[i-1]

    if elongateSNAKE:
        SNAKE.append(tempLastSnakePart)
        elongateSNAKE = False

    tempSnakeHead = [SNAKE[0][0] + SNAKE_FWD_VEC[0], SNAKE[0][1] + SNAKE_FWD_VEC[1]]
     #wrap snake coords
    if tempSnakeHead[0] > 10:
       tempSnakeHead[0] = 0

    if tempSnakeHead[0] < 0:
       tempSnakeHead[0] = 10

    if tempSnakeHead[1] > 9:
        tempSnakeHead[1] = 0

    if tempSnakeHead[1] < 0:
        tempSnakeHead[1] = 9
    

    if tempSnakeHead == SNAKE[2]:
        tempSnakeHead = [SNAKE[0][0] + BUFF_FWD_VEC[0], SNAKE[0][1] + BUFF_FWD_VEC[1]]
         #wrap snake coords again
        if tempSnakeHead[0] > 10:
            tempSnakeHead[0] = 0

        if tempSnakeHead[0] < 0:
           tempSnakeHead[0] = 10

        if tempSnakeHead[1] > 9:
            tempSnakeHead[1] = 0

        if tempSnakeHead[1] < 0:
            tempSnakeHead[1] = 9
    else:
        BUFF_FWD_VEC = list(SNAKE_FWD_VEC)

    SNAKE[0] = tempSnakeHead

   

    



def drawFrameBuffer(strip):
    drawnPixels = []
    for i in range(0, len(FRAMEBUFFER)):
        pixel = CLOCKMATRIX[FRAMEBUFFER[i][0]][FRAMEBUFFER[i][1]]
        strip.setPixelColor(pixel - 1, FRAMEBUFFER[i][2])

        drawnPixels.append(pixel - 1)

    for i in range(0, 110):
        if i not in drawnPixels:
            strip.setPixelColor(i, Color(0,0,0))

    strip.show()
    del FRAMEBUFFER[:]


def update(strip):
    global elongateSNAKE
    global dead

    if dead:
        colorWipe(strip, Color(0, 0, 255))
        reset()

    else:
        getInputVec()

        if appleEaten():
            spawnApple()
            elongateSNAKE = True

        moveSnake()

        if snakeBiteSelf():
            dead = True
        #snakeBiteSelf()

        renderSnake()
        renderApple()

        drawFrameBuffer(strip)

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# Main program logic follows:
if __name__ == '__main__':
   
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
 
    print ('Press Ctrl-C to quit.')
    
   
    try:
       while True:
           update(strip)
           time.sleep(1)

 
    except KeyboardInterrupt:
        if args.clear:
             colorWipe(strip, Color(0,0,0), 10)