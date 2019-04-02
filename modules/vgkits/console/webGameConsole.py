import socket

from vgkits.random import randint

htmlHead = b"""
<!DOCTYPE html>
<html>
    <head><title>Example page</title></head>
    <body>"""
htmlPreOpen = b"""<pre>"""
htmlPreClose = b"""</pre>"""
htmlForm = b"""<form method="GET" autocomplete="off"><input type="text" name="response" autofocus></form>"""
htmlBreak = b"<br/>"
htmlFoot = b"""
    </body>
</html>
"""

defaultHeaders = (
    b"HTTP/1.1 200 OK",
    b"Content-Type: text/html; charset=UTF-8",
    b"Connection: close",
)

crlf=b"\r\n"

def decodeuricomponent(string): # original from https://gitlab.com/superfly/dawndoor/blob/master/src/dawndoor/web.py
    string = string.replace('+', ' ')
    arr = string.split('%')
    arr2 = [chr(int(part[:2], 16)) + part[2:] for part in arr[1:]]
    return arr[0] + ''.join(arr2)


def hostGame(gameMaker, repeat=True, port=8080):

    gameMap = {}

    def getGame(cookie):
        try:
            return gameMap[cookie]
        except KeyError:
            return None

    def setGame(cookie, value):
        gameMap[cookie] = value
        return value

    try:
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)

        cl = None

        def show(text):
            textType = type(text)
            if textType is str:
                # TODO entity encode strings
                cl.send(text.encode('ascii'))
                cl.send(htmlBreak)
            elif textType is bytes:
                cl.send(text) # send bytestrings unencoded
            else:
                raise Exception('Cannot print object of type ' + str(textType))


        while True:
            try:

                response = None

                while True:
                    try:
                        cl, addr = s.accept()

                        cookie = None
                        resource = None

                        cl_file = cl.makefile('rwb', 0)
                        while True:
                            line = cl_file.readline()
                            if not line or line == b'\r\n':
                                break
                            else:
                                try:
                                    if line.startswith(b"GET"):
                                        (method, path, version) = line.split()
                                        if b"?" in path:
                                            resource, query = path.split(b"?")
                                            if b"response=" in query:
                                                _, response = path.split(b"response=")
                                                response = response.decode("ascii")
                                                response = decodeuricomponent(response)
                                        else:
                                            resource = path
                                    elif line.startswith(b"Cookie"):
                                        _, cookie = line.split(b":")
                                        cookie = cookie.strip()
                                        if cookie == b"":
                                            cookie = None
                                except ValueError:
                                    pass

                        for header in defaultHeaders:
                            cl.send(header)
                            cl.send(crlf)

                        if cookie is None:
                            cookie = str(randint(1000000000)).encode('ascii')
                            cl.send(b"Set-Cookie: ")
                            cl.send(cookie)
                            cl.send(crlf)

                        # repeated crlf means end of headers
                        cl.send(crlf)

                        cl.send(htmlHead)
                        cl.send(htmlPreOpen)

                        if resource == b"/":
                            game = getGame(cookie)
                            while True:
                                try:
                                    if game is None:
                                        game = setGame(cookie, gameMaker(show)) # create a new game
                                        prompt = game.send(None)  # generate next prompt, response not expected
                                    else:
                                        if response is not None:
                                            prompt = game.send(response)  # generate next prompt, response is expected
                                        else:
                                            pass # no response, serve previous prompt again
                                    cl.send(prompt.encode('ascii'))
                                    cl.send(htmlBreak)
                                    break
                                except StopIteration:
                                    if repeat:
                                        game = setGame(cookie, None)
                                        continue # create and run the game again
                                    else:
                                        cl.send("Game Over. Server closing".encode('ascii'))
                                        break
                                except Exception as e:
                                    show(e)

                        cl.send(htmlPreClose)
                        cl.send(htmlForm)
                        cl.send(htmlFoot)

                    finally:
                        cl.close()
                        cl = None
            finally:
                if not repeat:
                    break
    finally:
        s.close()


if __name__ == "__main__":
    from examples.hello import *
    hostGame(createHelloGame)    
