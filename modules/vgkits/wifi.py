import network

uplink = None
downlink = None

def mac():
    return network.WLAN().config('mac')  # 5 bytes


def identify(numBytes=None):
    import ubinascii
    add = mac()
    if numBytes == None:
        numBytes = len(add)
    return ubinascii.hexlify(add[-numBytes:])


def suffix():
    return identify(3)


def getUser():
    global uplink
    if uplink is None:
        uplink = network.WLAN(network.STA_IF)
    return uplink


def getUserAddress():
    uplink = getUser()
    if uplink.isconnected():
        return uplink.ifconfig()[0]
    else:
        return None


def useWifi(ssid, auth, timeout=16000):
    uplink = getUser()
    uplink.active(True)
    uplink.connect(ssid, auth)
    from time import ticks_diff, ticks_ms, sleep_ms
    started = ticks_ms()
    while True:
        if uplink.isconnected():
            print(getUserAddress())
            return uplink
        else:
            if ticks_diff(ticks_ms(), started) < timeout:
                sleep_ms(100)
                continue
            else:
                return None


def stopUsingWifi():
    uplink = getUser()
    uplink.active(False)


def getProvider():
    global downlink
    if downlink is None:
        downlink = network.WLAN(network.AP_IF)
    return downlink


def provideWifi(ssid, auth):
    downlink = getProvider()
    downlink.active(True)
    downlink.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=auth)
    return downlink


def provideInsecureWifi():
    return provideWifi(ssid='vanguard-{}'.format(suffix().decode('ascii')), auth="vanguard")


def stopProvidingWifi():
    downlink = getProvider()
    downlink.active(False)
