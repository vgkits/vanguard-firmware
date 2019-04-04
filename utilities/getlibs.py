import sys
import pip

def run():
    sys.argv="pip install pyserial esptool adafruit-ampy six rshell".split()
    pip.main()

if __name__ == "__main__":
    run()
