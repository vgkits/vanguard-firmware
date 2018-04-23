import sys
import pip

def run():
    sys.argv="pip install pyserial esptool adafruit-ampy".split()
    pip.main()

if __name__ == "__main__":
    run()