
# userver.py Demo of simple uasyncio-based echo server

# Released under the MIT licence
# Copyright (c) Peter Hinch 2019

import usocket as socket
import uasyncio as asyncio
import uselect as select

headers200 = b"""HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n"""

htmlHead = b"""
<!DOCTYPE html>
<html>
    <head><title>Example page</title></head>
    <body>"""

htmlFoot = b"""
    </body>
</html>
"""

response = None

class Server:
    async def run(self, loop, port=8123):
        addr = socket.getaddrinfo('0.0.0.0', port, 0, socket.SOCK_STREAM)[0][-1]
        s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # server socket
        s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_sock.bind(addr)
        s_sock.listen(5)
        self.socks = [s_sock]  # List of current sockets for .close()
        poller = select.poll()
        poller.register(s_sock, select.POLLIN)
        client_id = 1  # For user feedback
        while True:
            res = poller.poll(1)  # 1ms block
            if res:  # Only s_sock is polled
                c_sock, _ = s_sock.accept()  # get client socket
                loop.create_task(self.run_client(c_sock, client_id))
                client_id += 1
            await asyncio.sleep_ms(200)

    async def run_client(self, sock, cid):
        global response
        self.socks.append(sock)
        sreader = asyncio.StreamReader(sock)
        swriter = asyncio.StreamWriter(sock, {})
        path = None
        try:
            while True:
                line = await sreader.readline()
                if not line or line == b'\r\n':
                    break
                else:
                    try:
                        if line.startswith(b"GET"):
                            (method, path, version) = line.split()
                            if b"response=" in path:
                                _,response = path.split(b"response=")
                                response = decodeuricomponent(response)
                                response = response.decode("ascii")
                    except ValueError:
                        pass
            await swriter.awrite(headers200)
            await swriter.awrite(htmlHead)
            await swriter.awrite(b'Hello World')
            await swriter.awrite(htmlFoot)
        finally:
            sock.close()
            self.socks.remove(sock)

    def close(self):
        for sock in self.socks:
            sock.close()

loop = asyncio.get_event_loop()
server = Server()
try:
    loop.run_until_complete(server.run(loop))
except KeyboardInterrupt:
    print('Interrupted')  # This mechanism doesn't work on Unix build.
finally:
    server.close()
