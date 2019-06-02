import socket
import gc

from vgkits.random import randint
from vgkits.http.server.request import *

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
htmlResetForm = b"""<form method="POST" style="position:absolute; top:0px; right:0px" autocomplete="off"><button type="submit" name="reset" value="true">X</button></form>"""
htmlResponseForm = b"""<form method="POST" autocomplete="off"><input type="text" name="response" autofocus></form>"""
htmlBreak = b"<br/>"
htmlFoot = b"""
    </body>
</html>
"""

crlf=b"\r\n"


def decodeuricomponent(string): # original from https://gitlab.com/superfly/dawndoor/blob/master/src/dawndoor/web.py
    string = string.replace('+', ' ')
    arr = string.split('%')
    arr2 = [chr(int(part[:2], 16)) + part[2:] for part in arr[1:]]
    return arr[0] + ''.join(arr2)


def writeHttpHeaders(cl, status=b"200 OK", contentType=b"text/html", charSet=b"UTF-8"):
    if type(status) is not bytes:
        status = str(status).encode('utf-8')
    cl.send(b"HTTP/1.1 "); cl.send(status); cl.send(crlf)
    cl.send(b"Content-Type:"); cl.send(contentType); cl.send(b" ; charset="); cl.send(charSet); cl.send(crlf)
    cl.send(b"Connection: close"); cl.send(crlf)


def writeCookieHeaders(cl, requestMap):
    cookies = requestMap.get("cookies")
    if cookies is not None:
        cl.send(b"Set-Cookie: ")
        comma = False
        for cookieName, cookieValue in cookies.items():
            if comma:
                cl.send(b",")
            cl.send(cookieName)
            cl.send(b"=")
            cl.send(cookieValue)
            comma = True
        cl.send(crlf)


def writeHtmlBegin(cl):
    cl.send(htmlHead)
    cl.send(htmlResetForm)
    cl.send(htmlPreOpen)


def writeHtmlEnd(cl):
    cl.send(htmlPreClose)
    cl.send(htmlResponseForm)
    cl.send(htmlFoot)


def getCookie(requestMap, cookieName=b"session"):
    cookies = requestMap.get("cookies")
    if cookies is not None:
        cookieValue = cookies.get(cookieName)
        if cookieValue is not None:
            return cookieValue
    return None


def createCookie(requestMap, cookieName=b"session"):
    cookies = requestMap.get("cookies")
    if cookies is None:
        cookies = {}
        requestMap["cookies"] = cookies
    cookieValue = cookies.get(cookieName)
    if cookieValue is None:
        cookieValue = str(randint(1000000000)).encode('utf-8')
        cookies[cookieName] = cookieValue
    return cookieValue


def writeItem(cl, obj):
    cl.send(str(obj).encode('utf-8'))


gameMap = {}


def resetAllGames():
    global gameMap
    gameMap = {}


def getGame(cookie):
    return gameMap.get(cookie)


def setGame(cookie, value):
    if value is None:
        gameMap.pop(cookie, None)
    else:
        gameMap[cookie] = value
    return value


def hostGame(gameMaker, port=8080, repeat=True, resetAll=True, debug=False):

    if resetAll:
        resetAllGames()

    cl = None # doprint references this current client socket reference

    def doprint(*items, sep=b" ", end=b"\n"):
        """Equivalent to print, but writes to current client socket """
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

        while True: # handle requests from inbound client sockets one by one
            try:

                try:

                    gc.collect() # clear memory

                    cl, addr = s.accept()

                    requestMap = mapRequest(cl, debug)

                    if requestMap is None or requestMap == {}:
                        raise WebException("Request empty")

                    if debug:
                        print(requestMap)

                    resource = requestMap.get('resource')

                    sessionCookie = getCookie(requestMap)

                    reset = sessionCookie is None

                    if resource == b"/":

                        # process application state, render page

                        game = getGame(sessionCookie)

                        method = requestMap.get('method')
                        params = requestMap.get('params')

                        # reset logic
                        if method == b"GET":
                            if game is None:
                                reset = True
                            else:
                                raise BadRequestException("In-progress game: GET request invalid")
                        elif method == b"POST":
                            if params is not None:
                                if b"reset" in params:
                                    reset = True

                        if reset:
                            if sessionCookie is not None:
                                setGame(sessionCookie, None)
                            sessionCookie = createCookie(requestMap)
                            game = setGame(sessionCookie, gameMaker(doprint))
                        else:
                            game = getGame(sessionCookie)
                            if game is None:
                                raise BadRequestException("In-progress game not available")

                        response = None
                        if method == b"POST" and not reset:
                            if params is not None:
                                response = params.get(b"response")
                            if response is not None:
                                response = response.decode("utf-8")
                                response = decodeuricomponent(response)
                            elif not reset:
                                raise BadRequestException("In-progress game: POST without 'response' param invalid")

                        writeHttpHeaders(cl)

                        if reset:
                            writeCookieHeaders(cl, requestMap)

                        cl.send(crlf)  # finish headers

                        writeHtmlBegin(cl)

                        if debug:
                            doprint(str(requestMap))

                        while repeat:
                            try:
                                prompt = game.send(response)  # coroutine calls doprint closure on cl.send()
                                writeItem(cl, prompt)
                                cl.send(htmlBreak)
                                break
                            except StopIteration:
                                if repeat: # create and run the game again
                                    game = setGame(sessionCookie, gameMaker(doprint))
                                    response = None
                                    continue
                                else:
                                    cl.send(b"Game Over. Server closing")
                                    break

                        writeHtmlEnd(cl)

                        cl.close()
                        cl = None
                        continue

                    else: # unknown resource
                        raise NotFoundException("Unknown resource ", resource)

                except Exception as e: # intercept and write error page
                    if cl is not None:
                        if isinstance(e, WebException):
                            writeHttpHeaders(cl, status=e.status)
                        else:
                            writeHttpHeaders(cl, status=WebException.status)
                        writeHtmlBegin(cl)
                        cl.send(b"Error: ")
                        if isinstance(e, WebException):
                            cl.send(e.status)
                        cl.send(htmlBreak)
                        writeItem(cl, repr(e))
                        cl.send(htmlBreak)
                        cl.send(b"Reset session with X at top-right of this page")
                        writeHtmlEnd(cl)
                    raise
                finally:
                    if cl is not None:
                        try:
                            cl.close()
                        finally:
                            cl = None
            except Exception as e:
                print("Exception in " + __name__)
                print(repr(e))
    finally:
        s.close()
