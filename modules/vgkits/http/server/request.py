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
    method = None

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
                        _, headerValue = line.split(b":")
                        contentType, _ = line.split(b";")
                        contentType = contentType.strip()
                        requestMap.update(contentType=contentType)
                    elif line.startswith(b"Purpose: prefetch"):
                        requestMap.update(prefetch=True)
                except ValueError:
                    pass
        if method == "POST" and contentType is b"application/x-www-form-urlencoded": # extract keypairs from body
            while True:
                line = cl_file.readline()
                if debug:
                    print(line)
                if not line or line == b'\r\n':
                    break
                else: # expect body line to be 'query params'
                    requestMap.update(params = extractParams(line))


        return requestMap
