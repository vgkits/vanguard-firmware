#!/bin/sh
esptool.py --port /dev/ttyUSB0 --baud 1500000 write_flash 0x00000 extracted.img
