# TODO make https and http calls consistent with each other
# TODO implement as async generators?

def getHttps(url, headers=None):
    _, _, host, path = url.split('/', 3)
    import usocket
    import ussl
    import sys
    addr = usocket.getaddrinfo(host, 443)[0][-1] # TODO assumes IPv4
    s=usocket.socket()
    s.connect(addr)
    s.settimeout(1.0)
    try:
        s=ussl.wrap_socket(s)
        s.write(b'GET /{} HTTP/1.1\r\nHost: {}\r\nUser-Agent: vgkits.org\r\n'.format(path, host))
        if headers is not None:
            s.write(headers)
        s.write(b'\r\n')
        buf = bytearray(128)
        while True:
            try:
                count = s.readinto(buf) # TODO use readline for headers including e.g. 'content-length: 2358' then after blank line, count bytes before close
                if count > 0:
                    if count < len(buf):
                        sys.stdout.write(buf[:count])
                    else:
                        sys.stdout.write(buf)
                    continue
            except OSError as ose:
                print(ose)
            break
    finally:
        s.close()

def getHttp(url, headers=None):
    _, _, host, path = url.split('/', 3)
    import usocket
    import sys
    addr = usocket.getaddrinfo(host, 80)[0][-1] # TODO assumes IPv4
    s = usocket.socket()
    s.connect(addr)
    s.send(b'GET /{} HTTP/1.1\r\nHost: {}\r\nUser-Agent: vgkits.org\r\n'.format(path, host))
    if headers is not None:
        s.send(headers)
    s.send(b'\r\n')

    buf = bytearray(128)
    while True:
        try:
            count = s.readinto(buf) # TODO use readline for headers including e.g. 'content-length: 2358' then after blank line, count bytes before close
            if count > 0:
                if count < len(buf):
                    sys.stdout.write(buf[:count])
                else:
                    sys.stdout.write(buf)
                continue
        except OSError as ose:
            print(ose)
        break
    s.close()
