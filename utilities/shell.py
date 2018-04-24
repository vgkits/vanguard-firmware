import sys,os
from serial.tools import miniterm
import config, command

minicomCommand = "serial.tools.miniterm --raw --eol ${eol} --encoding ascii ${port} ${baud}"
minicomLookup = config.hardwareConfig()
minicomLookup.update( eol={'\n':'CR','\r\n':'CRLF'}.get(os.linesep))
command.emulateInvocation(minicomCommand, minicomLookup)
miniterm.main()