import socket
import os
import gc

hitcount = 0


def createServer(handler=None):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    serverSocket = socket.socket()
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(addr)
    serverSocket.listen(1)

    if handler:
        serverSocket.setsockopt(socket.SOL_SOCKET, 20, handler)

    print('listening on', addr)

    return serverSocket


def createZipClientHandler(filepath):
    filesize = os.stat(filepath)[6]
    headerBytes = b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Encoding: gzip\r\nContent-Length: '
    sizeBytes = b'%s' % filesize
    separatorBytes = b"\r\n\r\n"

    def zipClientHandler(serverSocket):
        clientSocket = None
        clientFile = None
        try:
            global hitcount

            clientSocket, addr = serverSocket.accept()
            # clientSocket.setblocking(False)

            hitcount += 1
            print('request %s' % hitcount)
            clientFile = clientSocket.makefile('rwb', 0)
            path = None
            while True:
                line = clientFile.readline()
                if line == b'\r\n': # SHOULD THIS READ if not line or line == b'\r\n':
                    break
                else:
                    try:
                        if line.startswith(b"GET"):
                            (method, path, version) = line.split()
                            if path != b"/":
                                path is None
                    except ValueError:
                        pass
            if path is not None:
                # write the HTTP headers
                clientSocket.write(headerBytes)
                clientSocket.write(sizeBytes)
                clientSocket.write(separatorBytes)
                # write the file bytes
                bufferLength = 512
                buffer = bytearray(bufferLength)
                with open(filepath, 'r') as f:
                    while True:
                        readLength = f.readinto(buffer)
                        if readLength == bufferLength:
                            clientSocket.write(buffer)
                        elif readLength > 0:
                            clientSocket.write(memoryview(buffer)[:readLength])
                        else:
                            break
        finally:
            if clientSocket is not None:
                clientSocket.close()
            if clientFile is not None:
                clientFile.close()
            gc.collect()

    return zipClientHandler

def run():
    import webrepl
    webrepl.start(password='vanguard')
    return createServer(createZipClientHandler("vgkits/util/webrepl-inlined.html.gz"))
