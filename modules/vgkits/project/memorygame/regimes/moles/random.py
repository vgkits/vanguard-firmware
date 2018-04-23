"""A random whack-a-mole, the next unlit light chosen at random"""

from vgkits.project.memorygame import *

def run():
    lit = None
    while True:
        available = []
        for index in range(4):
            lights[index].value(1)
            if index is not lit:
                available.append(index)
        lit = randint(len(available))
        lights[lit].value(0)
        while buttons[lit].value() is 1:
            pass

if __name__ == "__main__":
    run()