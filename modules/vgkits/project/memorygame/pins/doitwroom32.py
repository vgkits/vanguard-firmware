from machine import Pin, PWM
from vgkits.board.doitwroom32 import *

# ground sink pins for LEDs (positive pins are powered through a current-limiting resistor)
lights = [
    Pin(D12, mode=Pin.OUT, value=1),
    Pin(D32, mode=Pin.OUT, value=1),
    Pin(D19, mode=Pin.OUT, value=1),
    Pin(D2, mode=Pin.OUT, value=1),
]

# button input pins, (connected to +V through a pull-up resistor)
buttons = [
    Pin(D13, mode=Pin.IN, pull=None),
    Pin(VP, mode=Pin.IN, pull=None),
    Pin(D22, mode=Pin.IN, pull=None),
    Pin(D15, mode=Pin.IN, pull=None),
]

# extra button ground pins (created by inputs set to 0V)
grounds = [
    Pin(D18, mode=Pin.OUT, value=0),
    Pin(D33, mode=Pin.OUT, value=0),
]

# attached to a PiezoElectric Transceiver to make beeps
beeper = PWM(Pin(D19), freq=1000, duty=0)
