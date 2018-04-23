from time import sleep
from machine import Pin
from vgkits.ws2811 import *

num_pixels = 8
startPixels(pin=Pin(14), num=8)
allIndexes = range(num_pixels)
clearPixels()

# values controlling rainbow
# hue of first pixel
hueOffset = 0
hueSeparation = 1.0 / 8.0
darkFactor = 1 / 8.0
hueChange = 0.02
changeDelay = 0.02


def darken(rgb, proportion=0.05):
    return [int(value * proportion) for value in rgb]


def paintWheel():
    colors = [wheel(((i * hueSeparation) + hueOffset) % 1) for i in allIndexes]
    for i in allIndexes:
        setPixel(i, darken(colors[i], darkFactor), False)
    showPixels()


def rotateWheel():
    global hueOffset
    while True:
        paintWheel()
        sleep(changeDelay)
        hueOffset = hueOffset + hueChange


if __name__ == "__main__":
    paintWheel()