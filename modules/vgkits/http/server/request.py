class WebException(Exception):
    status = b"500 Internal Server Error"


class BadRequestException(WebException):
    status = b"400 Bad Request"


class NotFoundException(WebException):
    status = b"404 Not Found"


def extractParams(query):
    params = {}
    paramPairs = query.split(b"&")
    for paramPair in paramPairs:
        paramName, paramValue = paramPair.split(b"=")
        params[paramName] = paramValue
    return params


def extractCookies(cookieHeaderValue):
    cookies = {}
    cookiePairs = cookieHeaderValue.split(b";")
    for cookiePair in cookiePairs:
        cookieName, cookieValue = cookiePair.strip().split(b"=")
        cookies[cookieName] = cookieValue
    return cookies


def mapRequest(clientSocket, debug=False):
    """Consumes HTTP headers extracting GET and POST method, path, resource, param and cookie keypairs.
    Returns extracted values in a dict"""
    requestMap = dict()
    contentType = None
    contentLength = 0
    method = None

    clFile = clientSocket.makefile('rb', 0)
    try:
        try:
            while True:
                line = clFile.readline() # consider making lowercase before processing
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
                            if method == b"GET" and b"?" in path:
                                resource, query = path.split(b"?")
                                requestMap.update(resource=resource)
                                requestMap.update(params = extractParams(query))
                            else:
                                requestMap.update(resource=path)
                        elif line.startswith(b"Cookie:"):
                            _, cookieHeaderValue= line.split(b":")
                            requestMap.update(cookies = extractCookies(cookieHeaderValue))
                        elif line.startswith(b"Content-Type:"):
                            contentType = line.split(b":")[-1]
                            requestMap.update(contentType=contentType)
                        elif line.startswith(b"Content-Length:"):
                            contentLength = line.split(b":")[-1]
                            contentLength = int(contentLength) # TODO limit contentLength
                            requestMap.update(contentLength=contentLength)
                        elif line.startswith(b"Purpose: prefetch"):
                            requestMap.update(prefetch=True)
                    except ValueError:
                        pass
            if method == b"POST":
                if b"application/x-www-form-urlencoded" in contentType and contentLength > 0: # extract keypairs from body
                    line = clFile.read(contentLength)
                    if debug:
                        print(line)
                    requestMap.update(params = extractParams(line))
                else:
                    raise BadRequestException("POST not x-www-form-urlencoded")

        finally:
            import sys
            if hasattr(sys, 'implementation'): # mpy or py3
                name = sys.implementation.name
                if name == "micropython" or name == "circuitpython":
                    pass # s.makefile() was a no-op, closing file will close socket
                else:
                    clFile.close() # file is separate resource, can be closed

    except Exception as e:
        print("Exception in " + __name__)
        print(repr(e))

    return requestMap

