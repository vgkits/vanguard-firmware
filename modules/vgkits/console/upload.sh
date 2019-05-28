#!/bin/sh
ampy --port /dev/ttyUSB0 mkdir --exists-okay vgkits
ampy --port /dev/ttyUSB0 mkdir --exists-okay vgkits/console
rshell --ascii --buffer-size=30 --port /dev/ttyUSB0 rsync -v ./ /pyboard/vgkits/console
