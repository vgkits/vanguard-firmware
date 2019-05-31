#!/bin/sh
ampy --port /dev/ttyUSB0 mkdir --exists-okay vgkits
ampy --port /dev/ttyUSB0 mkdir --exists-okay vgkits/console
ampy --port /dev/ttyUSB0 mkdir --exists-okay vgkits/http
ampy --port /dev/ttyUSB0 mkdir --exists-okay vgkits/util
rshell --ascii --buffer-size=30 --port /dev/ttyUSB0 rsync -v ./vgkits/console /pyboard/vgkits/console
rshell --ascii --buffer-size=30 --port /dev/ttyUSB0 rsync -v ./vgkits/http /pyboard/vgkits/http
rshell --ascii --buffer-size=30 --port /dev/ttyUSB0 rsync -v ./vgkits/util /pyboard/vgkits/util
