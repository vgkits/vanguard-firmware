# based on shutil.py from micropython-lib originally authored by @pfalcon
import os

def rmtree(top):
    for path, dirs, files in os.walk(top, False):
        for f in files:
            os.unlink(path + "/" + f)
        os.rmdir(path)

def copyfileobj(src, dest, length=512):
    if hasattr(src, "readinto"):
        buf = bytearray(length)
        while True:
            sz = src.readinto(buf)
            if not sz:
                break
            if sz == length:
                dest.write(buf)
            else:
                b = memoryview(buf)[:sz]
                dest.write(b)
    else:
        while True:
            buf = src.read(length)
            if not buf:
                break
            dest.write(buf)


def copyfile(fromPath, toPath):
    with open(fromPath, 'rb') as fromFile:
        with open(toPath, 'wb') as toFile:
            copyfileobj(fromFile, toFile)