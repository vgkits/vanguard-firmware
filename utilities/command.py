import config

def guessDevice():
    import platform
    ostype = platform.system()
    if ostype == 'Linux':
        return "/dev/ttyUSB0"
    elif ostype == 'Darwin':
        return "/dev/tty.SLAB_USBtoUART"
    elif ostype == 'Windows':
        return None


device = None
def selectDevice():
    global device
    from six.moves import input
    from serial.tools.list_ports import comports

    availableDevices = [info.device for info in comports()]

    defaultDevice = guessDevice()

    message = "Type the number of the device: "
    if defaultDevice is not None:
        if defaultDevice not in availableDevices:
            print("No device {}. Plugged in? Drivers installed?".format(defaultDevice))
            defaultDevice = None

    if len(availableDevices) == 1:
        defaultDevice = availableDevices[0]

    if defaultDevice is not None:
        message += "({}) ".format(defaultDevice)

    while device is None:
        for index, item in enumerate(availableDevices):
            print("{} : {}".format(index, item))

        try:
            choice = input(message)
            if choice == "":
                if defaultDevice is not None:
                    device = defaultDevice
            else:
                device = availableDevices[int(choice)]
        except ValueError:
            print("Cannot accept {}".format(choice))
            pass

    return device


def detectBoardConfig():
    import sys
    import re
    import io
    import esptool
    oldOut = sys.stdout
    newOut = io.StringIO()
    emulateInvocation("esptool.py --port ${port} flash_id", config.hardwareConfig())
    try:
        sys.stdout = newOut
        esptool.main()
    finally:
        sys.stdout = oldOut

    printed = newOut.getvalue()
    def extractBackreference(pattern):
        return re.search(pattern, printed, re.MULTILINE).group(1)
    return {
        "chip": extractBackreference("^Chip is (\w+)$"),
        "manufacturer": extractBackreference('^Manufacturer: (\w+)$'),
        "device": extractBackreference('^Device: (\w+)$'),
        "flash_size": extractBackreference('^Detected flash size: (\w+)$'),
    }


def emulateInvocation(templateString, config):
    import sys
    import string
    command = string.Template(templateString).substitute(config)
    print("Running '" + command + "'")
    sys.argv = command.split()


def releaseBoard():
    from ampy import cli
    if cli._board is not None:
        try:
            cli._board.close()
        except:
            pass


def resetBoard():
    from config import hardwareConfig
    from ampy import pyboard, cli
    try:
        print('Resetting Board')
        emulateInvocation("ampy --port ${port} reset", hardwareConfig())
        try:
            cli.cli()
        except SystemExit:
            pass

    except pyboard.PyboardError:
        print("Is cockle unplugged or in use by another program?")

    releaseBoard()


def eraseBoard():
    import esptool
    emulateInvocation("esptool.py --port ${port} --baud ${baud} erase_flash", config.hardwareConfig())
    esptool.main()


def putFile(frompath, topath):
    from config import hardwareConfig
    from ampy import pyboard, cli
    try:
        putCommand = "ampy --port ${port} put ${frompath} ${topath}"
        putConfig = hardwareConfig()
        putConfig.update(
            frompath=frompath,
            topath=topath
        )
        emulateInvocation(putCommand, putConfig)
        try:
            cli.cli()
        except SystemExit:
            pass

    except pyboard.PyboardError:
        print("Is cockle unplugged or in use by another program?")

    releaseBoard()

# precede sync by
# ampy --port /dev/ttyUSB0 mkdir --exists-okay vgkits
# rshell --ascii --buffer-size=30 --port /dev/ttyUSB0 rsync ../modules/vgkits/ /pyboard/vgkits/
def rsync(fromdir, todir):
    params = config.hardwareConfig()
    params.update(
        fromdir=fromdir,
        todir=todir
    )

    # run ampy to lazy-create target directory if needed
    if todir != '' and todir != '/':
        from ampy import pyboard, cli
        try:
            emulateInvocation("ampy --port ${port} mkdir --exists-okay ${todir}", params)
            try:
                cli.cli()
            except SystemExit:
                pass
        except pyboard.PyboardError:
            print("Is cockle unplugged or in use by another program?")
            return

    # run rshell to recursively 'rsync' the folder
    import rshell.main
    try:
        emulateInvocation("rshell --ascii --buffer-size=30 --port ${port} rsync ${fromdir} /pyboard/${todir}", params)
        rshell.main.main()
    finally:
        pass