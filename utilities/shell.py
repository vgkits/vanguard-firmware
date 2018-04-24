import sys
from serial.tools import miniterm
import config, command

minicomCommand = "serial.tools.miniterm --raw --encoding ascii ${port} ${baud}"
minicomLookup = config.hardwareConfig()
command.emulateInvocation(minicomCommand, minicomLookup)
miniterm.main()