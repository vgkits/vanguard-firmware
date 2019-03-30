def decodeuricomponent(string): # original from https://gitlab.com/superfly/dawndoor/blob/master/src/dawndoor/web.py
    string = string.replace('+', ' ')
    arr = string.split('%')
    arr2 = [chr(int(part[:2], 16)) + part[2:] for part in arr[1:]]
    return arr[0] + ''.join(arr2)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

lines = []

def inputFromWeb():
    global s, lineGenerator 
    lines.append( (yield None) )
    while True:
        try:
            cl, addr = s.accept()
            path = None
            cl_file = cl.makefile('rwb', 0)
            while True:
                line = cl_file.readline()
                if not line or line == b'\r\n':
                    break
                else:
                    try:
                        if line.startswith(b"GET"):
                            (method, path, version) = line.split()
                            if b"response=" in path:
                                _,response = path.split(b"response=")
                                response = response.decode("ascii")
                                response = decodeuricomponent(response)
                                lines.append( (yield response) )
                    except ValueError:
                        pass
            cl.send(head)
            for line in lines:
                cl.send(line)
                cl.send(b'<br>')
            lines[:] = []
            cl.send(foot)
        finally:
            cl.close()

def outputToWeb(lineGenerator):
    for line in lineGenerator:
        lines.append(line.encode('ascii'))

def hostInWeb(gameFactory):
    user = inputFromWeb()
    next(user) # skip initial empty user response
    game = gameFactory(user)
    outputToWeb(game)
