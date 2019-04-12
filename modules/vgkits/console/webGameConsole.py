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


def hostGame(gameMaker, repeat=True, port=8080, debug=False):

    gameMap = {}

    cl = None

    def getGame(cookie):
        try:
            return gameMap[cookie]
        except KeyError:
            return None

    def setGame(cookie, value):
        gameMap[cookie] = value
        return value

    def doprint(*items, sep=b" ", end=b"\n"):
        if type(sep) is str:
            sep = sep.encode('ascii')
        if type(end) is str:
            end = end.encode('ascii')
        if end == b"\n":
            end = htmlBreak
        try:
            prev = None
            for item in items:
                if prev is not None:
                    cl.send(sep)
                itemType = type(item)
                if itemType is str: # TODO entity encode strings?
                    item = item.encode('ascii')
                elif itemType is bytes:
                    pass # send bytestrings unencoded
                else:
                    raise Exception('Cannot coerce {} to bytes'.format(itemType))
                cl.send(item)
                prev = item
            cl.send(end)
        except OSError as e:
            print(str(e))

    # set up a server socket
    try:
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)

        # work out why games break if they don't have two question (don't end with a press enter to reset)
        while True:
            try:

                response = None

                while True:
                    try:
                        # handle client sockets one by one
                        cl, addr = s.accept()

                        cookies = {}
                        resource = None

                        cl_file = cl.makefile('rwb', 0)
                        while True:
                            line = cl_file.readline()
                            if debug:
                                print(line)
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
                                    elif line.startswith(b"Cookie:"):
                                        _, cookieList = line.split(b":")
                                        cookieList = cookieList.split(b";")
                                        for cookie in cookieList:
                                            cookieName, cookieValue = cookie.strip().split(b"=")
                                            cookies[cookieName] = cookieValue
                                except ValueError:
                                    pass

                        if debug:
                            print("Cookies:")
                            print(str(cookies))

                        for header in defaultHeaders:
                            cl.send(header)
                            cl.send(crlf)

                        if b"player" in cookies:
                            playerCookie = cookies[b"player"]
                        else: # allocate random player number
                            playerCookie = str(randint(1000000000)).encode('ascii')
                            cl.send(b"Set-Cookie: player=")
                            cl.send(playerCookie)
                            cl.send(crlf)

                        # repeated crlf means end of headers
                        cl.send(crlf)

                        cl.send(htmlHead)
                        cl.send(htmlPreOpen)

                        if resource == b"/":
                            game = getGame(playerCookie)
                            while True:
                                try:
                                    if game is None:
                                        game = setGame(playerCookie, gameMaker(doprint)) # create a new game
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
                                        game = setGame(playerCookie, None)
                                        continue # create and run the game again
                                    else:
                                        cl.send("Game Over. Server closing".encode('ascii'))
                                        break

                        cl.send(htmlPreClose)
                        cl.send(htmlForm)
                        cl.send(htmlFoot)

                    except Exception as e:
                        print(e)
                    finally:
                        if cl is not None:
                            cl.close()
                            cl = None
            finally:
                if not repeat:
                    break
    finally:
        s.close()
