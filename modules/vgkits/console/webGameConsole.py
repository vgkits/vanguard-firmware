import socket

from vgkits.random import randint

htmlHead = b"""
<!DOCTYPE html>
<html>
    <head>
        <title>Example page</title>
        <style>
            pre {
                overflow-x: auto;
                white-space: pre-wrap;
                white-space: -moz-pre-wrap;
                white-space: -pre-wrap;
                white-space: -o-pre-wrap;
                word-wrap: break-word;
            }
        </style>
    </head>
    <body>"""
htmlPreOpen = b"""<pre>"""
htmlPreClose = b"""</pre>"""
htmlResetForm = b"""<form method="GET" style="position:absolute; top:0px; right:0px" autocomplete="off"><button type="submit" name="reset" value="true">X</button></form>"""
htmlResponseForm = b"""<form method="GET" autocomplete="off"><input type="text" name="response" autofocus></form>"""
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


def mapRequest(clientSocket, debug=False):
    """Consumes HTTP headers extracting GET and POST method, path, resource, param and cookie keypairs.
    Returns extracted values in a dict"""
    cookies = {}
    params = {}
    requestMap = dict(
        params = params,
        cookies = cookies,
    )

    with clientSocket.makefile('rb', 0) as cl_file:
        while True:
            line = cl_file.readline()
            if debug:
                print(line)
            if not line or line == b'\r\n':
                break
            else:
                try:
                    if line.startswith(b"GET") or line.startswith(b"POST"):
                        (method, path, version) = line.split()
                        requestMap.update(
                            method=method,
                            path=path,
                        )
                        if b"?" in path:
                            resource, query = path.split(b"?")
                            requestMap.update(resource=resource)
                            paramPairs = query.split(b"&")
                            for paramPair in paramPairs:
                                paramName, paramValue = paramPair.split(b"=")
                                params[paramName] = paramValue

                        else:
                            requestMap.update(resource=path)
                    elif line.startswith(b"Cookie:"):
                        _, cookiePairs = line.split(b":")
                        cookiePairs = cookiePairs.split(b";")
                        for cookiePair in cookiePairs:
                            cookieName, cookieValue = cookiePair.strip().split(b"=")
                            cookies[cookieName] = cookieValue
                    elif line.startswith(b"Content-Type:"):
                        _, headerValue = line.split(b":")
                        contentType, _ = line.split(b";")
                        contentType = contentType.strip()
                        requestMap.update(contentType=contentType)
                    elif line.startswith(b"Purpose: prefetch"):
                        requestMap.update(prefetch=True)
                except ValueError:
                    pass

        return requestMap


def hostGame(gameMaker, repeat=True, port=8080, debug=False):

    gameMap = {}

    cl = None

    def getGame(cookie):
        return gameMap.get(cookie)

    def setGame(cookie, value):
        if value is None:
            del gameMap[cookie]
        else:
            gameMap[cookie] = value
        return value

    def resetGame(cookie): # dispose server-side session
        setGame(playerCookie, None)

    def doprint(*items, sep=b" ", end=b"\n"):
        if type(sep) is str:
            sep = sep.encode('utf-8')
        if type(end) is str:
            end = end.encode('utf-8')
        if end == b"\n":
            end = htmlBreak
        try:
            prev = None
            for item in items:
                if prev is not None:
                    cl.send(sep)
                itemType = type(item)
                if itemType is str: # TODO entity encode strings?
                    item = item.encode('utf-8')
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

        # work out why games break if they don't have two questions (don't end with a press enter to reset)
        while True:
            try:

                while True:
                    try:
                        # handle client sockets one by one
                        cl, addr = s.accept() # doprint binding relies on closure of `cl` reference

                        requestMap = mapRequest(cl, debug)

                        if debug:
                            print(requestMap)

                        resource = requestMap.get('resource')
                        params = requestMap.get('params')
                        cookies = requestMap.get('cookies')

                        if resource == b"/":

                            for header in defaultHeaders:
                                cl.send(header)
                                cl.send(crlf)

                            playerCookie = cookies.get(b"player")
                            if playerCookie is None:
                                playerCookie = str(randint(1000000000)).encode('utf-8')
                                cl.send(b"Set-Cookie: player=")
                                cl.send(playerCookie)
                                cl.send(crlf)

                            cl.send(crlf) # finish headers

                            # start the HTML page
                            cl.send(htmlHead)
                            cl.send(htmlResetForm)
                            cl.send(htmlPreOpen)

                            # process application state, render page

                            if b"reset" in params:
                                resetGame(playerCookie)

                            response = params.get(b"response")
                            if response is not None:
                                response = response.decode("utf-8")
                                response = decodeuricomponent(response)

                            game = getGame(playerCookie)
                            while True:
                                print("Entering game turn")
                                if debug:
                                    doprint(str(requestMap))
                                try:
                                    if game is None:
                                        game = setGame(playerCookie, gameMaker(doprint)) # create a new game
                                        prompt = game.send(None)  # generate next prompt, response not expected
                                    else:
                                        if response is not None:
                                            prompt = game.send(response)  # generate next prompt, response is expected
                                        else:
                                            pass # no response, serve previous prompt again
                                    cl.send(prompt.encode('utf-8'))
                                    cl.send(htmlBreak)
                                    break
                                except StopIteration:
                                    if repeat:
                                        game = setGame(playerCookie, None)
                                        continue # create and run the game again
                                    else:
                                        cl.send(b"Game Over. Server closing")
                                        break

                            cl.send(htmlPreClose)
                            cl.send(htmlResponseForm)
                            cl.send(htmlFoot)
                        else: # unknown resource
                            for header in defaultHeaders:
                                if b"200 OK" in header: # use 404 code instead of 200
                                    cl.send(b"HTTP/1.1 404 Not Found")
                                else:
                                    cl.send(header)
                                cl.send(crlf)
                            cl.send(crlf) # finish headers
                            cl.send(b"Unknown resource : ")
                            if type(resource) is bytes:
                                cl.send(resource)

                    except BrokenPipeError as bpe:
                        print("Broken Pipe Error")
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
