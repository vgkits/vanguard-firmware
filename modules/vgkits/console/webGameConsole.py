import socket

headers200 = b"""HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"""

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


def decodeuricomponent(string): # original from https://gitlab.com/superfly/dawndoor/blob/master/src/dawndoor/web.py
    string = string.replace('+', ' ')
    arr = string.split('%')
    arr2 = [chr(int(part[:2], 16)) + part[2:] for part in arr[1:]]
    return arr[0] + ''.join(arr2)


def hostGame(gameMaker, repeat=True, port=8080):
    try:
        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        cl = None
        def show(text):
            cl.send(text.encode('ascii'))
            cl.send(htmlBreak)

        while True:
            try:
                game = gameMaker(show)

                response = None
                prompt = None

                requestCount = 0
                while True:
                    try:
                        cl, addr = s.accept()

                        resource = None

                        cl_file = cl.makefile('rwb', 0)
                        prefetch = False
                        while True:
                            line = cl_file.readline()
                            print("L:", end="")
                            print(line)
                            if not line or line == b'\r\n':
                                break
                            else:
                                try:
                                    # TODO do not perform logic if you see header b'Purpose: prefetch\r\n' which is chrome prefetching (user won't see it)
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

                                        requestCount += 1
                                        print(f"Request {requestCount} is for resource {resource}")


                                    elif line.startswith(b"Purpose: prefetch"):
                                        prefetch = True
                                except ValueError:
                                    pass

                        cl.send(headers200)
                        cl.send(htmlHead)
                        cl.send(htmlPreOpen)

                        if resource == b"/":
                            if response is not None and prompt is not None:
                                print("Response triggered by previous prompt")
                                prompt = game.send(response)    # response prompted - pass to game
                            else:
                                print("No response or no previous prompt")
                                prompt = game.send(None)        # response not prompted - send None

                        if prompt:
                            cl.send(prompt.encode('ascii'))
                            cl.send(htmlBreak)
                        cl.send(htmlPreClose)
                        cl.send(htmlForm)
                        cl.send(htmlFoot)

                    finally:
                        cl.close()
                        cl = None
            except StopIteration:
                pass
            finally:
                if not repeat:
                    break
    finally:
        s.close()


if __name__ == "__main__":
    from examples.hello import *
    hostGame(createHelloGame)    
