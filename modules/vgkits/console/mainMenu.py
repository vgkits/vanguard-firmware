from vgkits.console.webGameConsole import hostGame
from vgkits.console.examples.menu import createSequence

def run():
    hostGame(createSequence, port=8080, repeat=True, debug=False)

if __name__ == "__main__":
    run()
