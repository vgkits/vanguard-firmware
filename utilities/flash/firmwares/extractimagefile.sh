#!/bin/sh
esptool.py --port /dev/ttyUSB0 --baud 1500000 read_flash 0x00000 0x100000 extracted.img
