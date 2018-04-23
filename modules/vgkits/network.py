def wifiConnect(ssid,auth,timeout=16000):
    from network import WLAN, STA_IF, AP_IF
    uplink = WLAN(STA_IF)
    uplink.active(True)
    uplink.connect(ssid, auth)
    started= ticks_ms()
    while True:
        if uplink.isconnected():
            return uplink
        else:
            if ticks_diff(ticks_ms(), started) < timeout:
                sleep_ms(100)
                continue
            else:
                return None

def mac():
    from network import WLAN
    nw = WLAN()
    return nw.config('mac')  # 5 bytes


def identify(numBytes=None):
    import ubinascii
    add = mac()
    if numBytes == None:
        numBytes = len(add)
    return ubinascii.hexlify(add[-numBytes:])


def suffix():
    return identify(3)
