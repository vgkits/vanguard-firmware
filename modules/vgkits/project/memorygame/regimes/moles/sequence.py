"""An orderly whack-a-mole, each light in sequence"""

from vgkits.project.memorygame import *

def run():
    for pos in range(0, 4):
        lights[pos].value(1)  # turn off light
    while True:
        for pos in range(0, 4):  # for each light
            lights[pos].value(0)  # turn on light
            while not buttons[pos].value() == 0:  # await matching button
                pass
            lights[pos].value(1)  # turn off


if __name__ == "__main__":
    run()
