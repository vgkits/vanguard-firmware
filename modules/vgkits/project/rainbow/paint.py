from time import sleep
from machine import Pin
from vgkits.ws2811 import *

pixels = startPixels(pin=Pin(14), num=8)
numPixels = pixels.n
clearPixels()

# values controlling rainbow
# hue of first pixel
hueOffset = 0
hueSeparation = 1.0 / 8.0
defaultBrightness = 1.0 / 8.0
hueChange = 0.02
changeDelay = 0.02

def darkenRgb(rgb, brightness=None):
    if brightness is None:
        brightness=defaultBrightness
    return [int(value * brightness) for value in rgb]

def fillSpectrum(count=None):
    if count is None:
        count = numPixels
    return [wheel(((i * hueSeparation) + hueOffset) % 1) for i in range(count)]


def darkSpectrum(count=None, brightness=None):
    return [darkenRgb(color, brightness) for color in fillSpectrum(count)]


def paintSpectrum(brightness=None):
    colors = darkSpectrum(brightness=brightness)
    for i in range(numPixels):
        setPixel(i, colors[i], False)
    showPixels()

def rotateSpectrum():
    global hueOffset
    while True:
        paintSpectrum()
        sleep(changeDelay)
        hueOffset = hueOffset + hueChange


def glimpseSpectrum():
    colors = darkSpectrum()
    for offset in range(-numPixels, numPixels):
        clearPixels(show=False)
        for pixel in range(numPixels):
            colorPos = pixel + offset
            if colorPos // 8 == 0:  # ignore painting below pixel -1 or above pixel 8
                setPixel(pixel, colors[colorPos], show=False)
        showPixels()
        sleep(changeDelay)
    clearPixels()

# support legacy name
rainbow = paintSpectrum

if __name__ == "__main__":
    glimpseSpectrum()
