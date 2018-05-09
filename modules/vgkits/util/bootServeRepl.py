import sys

try:
    import usocket as socket
except:
    import socket

import os

import gc

gc.collect()

import webrepl

try:
    webrepl.start(password='vanguard')

    replpath = "vgkits/util/webrepl-inlined.html.gz"

    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 80)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)  # TODO investigate optimal backlog number

    def accept_handler(sock):
        res = sock.accept()
        # print("Handling")
        client_s = res[0]
        # print("Request:" + string_request)
        try:
            path = None
            partialLine = ""
            while path is None:
                request = client_s.recv(2048).decode('utf-8')
                if request == "":
                    continue
                else:
                    lines = request.split("\r\n")
                    if len(lines) == 1: # no newline yet
                        partialLine += lines[0]
                        continue
                    else:
                        if partialLine != "":
                            lines[0] = partialLine + lines[0]
                        getLine = lines[0]
                        getLine = getLine.split()  # separate by whitespace
                        (request_method, path, request_version) = getLine
            header = ''
            if request_method == "GET" and "favicon" not in path:
                # print("GET "+ path)
                header += 'HTTP/1.1 200 OK\r\n'
                header += 'Content-Type: text/html; charset=UTF-8\r\n'
                header += 'Content-Encoding: gzip\r\n'

                replsize = os.stat(replpath)[6]
                header += 'Content-Length: ' + str(replsize) + '\r\n'
                header += '\r\n'

                client_s.write(header.encode('ascii'))

                bufferLength = 512
                buffer = bytearray(bufferLength)
                with open(replpath, 'r') as f:
                    while True:
                        readLength = f.readinto(buffer)
                        if readLength == bufferLength:
                            client_s.write(buffer)
                        elif readLength > 0:
                            client_s.write(memoryview(buffer)[:readLength])
                        else:
                            break
        except Exception as e:
            sys.print_exception(e)
        finally:
            client_s.close()


    s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)

except OSError as e:
    print("Full poweroff required. WebREPL not reloaded.")

gc.collect()
