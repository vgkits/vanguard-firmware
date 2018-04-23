import esptool
import config
import command
from config import flashSpeedOverride


# do the write
def flashFirmware(firmwarePath=None):
    boardParams = command.detectBoardConfig()

    for referenceName,referenceParams in config.boardTypes.items():
        if all([referenceParams[key]==boardParams[key] for key in ["manufacturer", "device", "flash_size"]]):
            flashParams = referenceParams
            print("Detected " + referenceName)
            break
    else:
        flashParams = None

    if flashParams is not None:
        params = dict()
        params.update(config.hardwareConfig())
        params.update(config.filesystemConfig())
        params.update(flashSpeedOverride)
        params.update(flashParams)
        if firmwarePath is not None:
            params['local_image_path'] = firmwarePath
        commandPattern = "esptool.py --port ${port} --baud ${baud} write_flash --flash_mode ${flash_mode} --flash_size ${flash_size} 0 ${local_image_path}"
        command.emulateInvocation(commandPattern, params)
        esptool.main()
    else:
        raise Error("Board unrecognised")

def run():
    command.eraseBoard()
    flashFirmware()


if __name__ == "__main__":
    run()
