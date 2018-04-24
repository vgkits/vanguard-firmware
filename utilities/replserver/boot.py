try:
    import usocket as socket
except:
    import socket

import os

import gc

gc.collect()

import webrepl

webrepl.start(password='vanguard')

replpath = "webrepl-inlined.html.gz"

s = socket.socket()
ai = socket.getaddrinfo("0.0.0.0", 80)
addr = ai[0][-1]

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)

def accept_handler(sock):
    res = sock.accept()
    # print("Handling")
    client_s = res[0]
    string_request = client_s.recv(2048).decode('utf-8')
    # print("Request:" + string_request)
    try:
        request_line = string_request.split("\r\n")[0]  # only consider first line
        request_line = request_line.split()  # separate by whitespace
        (request_method, path, request_version) = request_line
        header = ''
        content = ''
        if request_method == "GET" and "favicon" not in path:
            # print("GET "+ path)
            header += 'HTTP/1.1 200 OK\r\n'
            header += 'Content-Type: text/html; charset=UTF-8\r\n'
            header += 'Content-Encoding: gzip\r\n'

            replsize = os.stat(replpath)[6]
            header += 'Content-Length: ' + str(replsize) + '\r\n'
            header += '\r\n'

            client_s.send(header)

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
        print("Exception", e)
    finally:
        client_s.close()


s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)

gc.collect()
