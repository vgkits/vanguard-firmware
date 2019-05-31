html = b"""<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> 
        <p> %s </h1>
    </body>
</html>
"""

import socket
import gc

hitcount = 0

def monitorRequests(handler=None):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    serverSocket = socket.socket()
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(addr)
    serverSocket.listen(1)
    
    if handler:
        serverSocket.setsockopt(socket.SOL_SOCKET, 20, handler)

    print('listening on', addr)
    
    return serverSocket

def handleRequest(serverSocket):
    clientSocket = None
    clientFile = None
    try:
        global hitcount

        clientSocket, addr = serverSocket.accept()
        #clientSocket.setblocking(False)

        print('request %s' % hitcount)
        clientFile = clientSocket.makefile('rwb', 0)
        path = None
        while True:
            line = clientFile.readline()
            if line == b'\r\n':
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
            hitcount += 1
            clientSocket.send(html % hitcount)
    finally:
        if clientSocket is not None:
            clientSocket.close()
        if clientFile is not None:
            clientFile.close()
        gc.collect()


def serveForeground():
    serverSocket = monitorRequests()
    while True:
        handleRequest(serverSocket)


def serveBackground():
    serverSocket = monitorRequests(handleRequest)
    return serverSocket
    

def run():
    serverSocket = serveBackground()

    from time import sleep
    while True:
        sleep(10)
        print("Heartbeat")


if __name__ == "__main__":
    run()
