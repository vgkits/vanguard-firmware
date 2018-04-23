import os

"""The folder containing this config.py file - used to calculate relative paths"""
scriptFolder = os.path.dirname(os.path.realpath(__file__))

"""Default baud rate for ESP boards"""
baud = 115200

"""Override for using esptool to make flashing faster"""
flashSpeedOverride = dict(
    baud=1500000
)

"""Remote folder containing Micropython Firmware images"""
micropythonRemoteFolder = "http://micropython.org/resources/firmware/"

# Uncomment the Micropython image name that you wish to download and flash
# micropythonFirmwareName = "adafruit-circuitpython-feather_huzzah-2.2.3.bin"
# micropythonFirmwareName = "firmware-combined.bin"
# micropythonFirmwareName = "esp8266-20170108-v1.8.7.bin"
micropythonFirmwareName = "esp8266-20171101-v1.9.3.bin"

mainPath = "../modules/vgkits/project/rainbow/paint.py"

# TODO, see if uploadCommand can be in common between all boards (with parameters passed via string.Template)
boardTypes = {
    "nodemcu_m": {
        "manufacturer": "51",
        "device": "4014",
        "flash_size": "1MB",
        "flash_mode":"dout",
        "upload_command": "esptool.py --port ${port} --baud ${baud} write_flash --flash_mode ${flash_mode} --flash_size ${flash_size} 0x0000 ${local_image_file}",
    },
    "esp01_1M": {
        "manufacturer": "ef",
        "device": "4014",
        "flash_size": "1MB",
        "flash_mode":"dio",
        "upload_command":"esptool.py --port ${port} --baud ${baud} write_flash --flash_mode ${flash_mode} --flash_size=${flash_size} 0x0000 ${local_image_file}"
    },
    "nodemcu_v2_amica": {
        "manufacturer": "ef",
        "device": "4016",
        "flash_size": "4MB",
        "flash_mode": "qio", # Pretty sure NodeMCU v2 is qio
        "upload_command": "esptool.py --port ${port} --baud ${baud} write_flash --flash_size=${flash_size} 0 ${local_image_file}"
    },
}

# TODO: Consider policy for caching results from xxxConfig() calls

def retrievalConfig():
    filesystem_lookup = filesystemConfig()
    return dict(filesystem_lookup,
        remote_image_url=micropythonRemoteFolder + micropythonFirmwareName
    )


def filesystemConfig():
    return dict(
        local_image_path=scriptFolder + "/flash/firmwares/" + micropythonFirmwareName
    )

def hardwareConfig(port=None):
    if port is None:
        from command import selectDevice
        port = selectDevice()
    return dict(
        baud=baud,
        port=port
    )
