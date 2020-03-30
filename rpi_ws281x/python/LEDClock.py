
#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
 
import time
import datetime
from neopixel import *
import argparse
 
# LED strip configuration:
LED_COUNT      = 110      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 144     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
 
LAST_MINUTE_ENTRY = 0;

#All words on the clock
ES = [10, 11]
IST = [31, 50, 51]
FUENF = [71, 90, 91, 110]
ZEHN = [9, 12, 29, 32]
VIERTEL = [48, 53, 68, 73, 88, 93, 108]
ZWANZIG = [49, 52, 69, 72, 89, 92, 109]
DREIVIERTEL = [8, 13, 28, 33, 48, 53, 68, 73, 88, 93, 108]
VOR = [7, 14, 27]
NACH = [74, 87, 94, 107]
HALB = [6, 15,  26, 35]
H_ELF = [55, 66, 75]
H_FUENF = [75, 86, 95, 106]
H_EINS = [5, 16, 25, 36]
H_EIN = [5, 16, 25]
H_ZWEI = [76, 85, 96, 105]
H_DREI = [4, 17, 24, 37] 
H_VIER = [77, 84, 97, 104]
H_SECHS = [3, 18, 23, 38, 43]
H_ACHT = [78, 83, 98, 103]
H_SIEBEN = [2, 19, 22, 39, 42, 59]
H_ZWOELF = [62, 79, 82, 99, 102]
H_ZEHN = [ 1, 20, 21, 40]
H_NEUN = [40, 41, 60, 61]
UHR = [81, 100, 101]

def convertTimeToArray(strip):
    now = datetime.datetime.now()
    min = LAST_MINUTE_ENTRY
    hour = now.hour
    array = []
    if hour == 4 and min == 20 or hour == 16 and min == 20: #embrace 420
        rainbow(strip)
   # if hour < 8: #turn clock off from 0 to 8 in the morning
     #   return array;
    if min == 0: #new hour, let's have fun
        theaterChase(strip, Color(127,127,127), 50, 30)
    array = array + ES + IST + getMinuteArray()
    if min == 0:
        array = array + getHourArray(hour, True) + UHR
    elif min <= 20:
        array = array + getHourArray(hour, False)
    else:
        array = array + getHourArray(hour + 1, False)
    
    return array

def getHourArray(hour, fullTime):

	if hour > 12:
		hour = hour - 12
	if hour == 0:
		return H_ZWOELF
	if hour == 1:
		if fullTime:
			return H_EIN
		return H_EINS
	if hour == 2:
		return H_ZWEI
	if hour == 3:
		return H_DREI
	if hour == 4:
		return H_VIER
	if hour == 5:
		return H_FUENF
	if hour == 6:
		return H_SECHS
	if hour == 7:
		return H_SIEBEN
	if hour == 8:
		return H_ACHT
	if hour == 9:
		return H_NEUN
	if hour == 10:
		return H_ZEHN
	if hour == 11:
		return H_ELF
	if hour == 12:
		return H_ZWOELF
	return []

	

#get minutes	
def getMinuteArray():
	min = LAST_MINUTE_ENTRY
	if min == 0:
		return []
	if min == 5:
		return FUENF + NACH
	if min == 10:
		return ZEHN + NACH
	if min == 15:
		return VIERTEL + NACH
	if min == 20:
		return ZWANZIG + NACH
	if min == 25:
		return FUENF + VOR + HALB
	if min == 30:
		return HALB
	if min == 35:
		return FUENF + NACH + HALB
	if min == 40:
		return ZEHN + NACH + HALB
	if min == 45:
		return DREIVIERTEL
	if min == 50:
		return ZEHN + VOR
	if min == 55:
		return FUENF + VOR
	return []
	


#Show array
def showArray(strip, color, array):
	for i in range(strip.numPixels()):
		if array.__contains__(i + 1):
			strip.setPixelColor(i, color)
		else:
			strip.setPixelColor(i, Color(0,0,0))
	strip.show()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
 
# Returns true every time a new 5 minutes have started on the clock
# i.E it's now 00:35 or 00:10 
def timeHasChanged(isStartup):
    global LAST_MINUTE_ENTRY
    now = datetime.datetime.now()
    if isStartup == True:
        LAST_MINUTE_ENTRY = round(now.minute / 5) * 5 #round to nearest five
        return True
    if LAST_MINUTE_ENTRY != now.minute:
        if now.minute % 5 == 0:
            LAST_MINUTE_ENTRY = now.minute
            return True
    return False

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

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0) 

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
 
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
 
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    timeHasChanged(True)
    array = convertTimeToArray(strip)
    
    showArray(strip, Color(50,50,50), array)
 
    try:
       while True:
            if timeHasChanged(False) == True:
                 array = convertTimeToArray(strip)
                 showArray(strip, Color(50,50,50), array)
            else:
                time.sleep(30)
 
    except KeyboardInterrupt:
        if args.clear:
             colorWipe(strip, Color(0,0,0), 10)

