import sys


def printShow(text):
    """Causes a line of game text to appear"""
    print(text)


def hostGame(gameMaker, repeat=False):
    """
        Hosts a game, showing output and receiving input through the text console.

        It accepts a gameMaker function. This should be a generator function (a
        function which uses the yield keyword).

        The generator function will be called passing a `show` function as a parameter.

        Within gameMaker, show() can be called to make lines of text appear for the user.

        A question prompting the user can be passed at any point in the game sequence with a
        yield expression. The value of the yield expression will be what the user typed
        in response to the text prompt.

        For example this would define a simple game which will run forever...

        def createHelloGame(show):
            while True:
                show("Welcome to the game")
                username = yield "What is your name? "
                show("Hello " + username)
                yield "Press enter to restart the game "

        hostGame(createHelloGame)

        :param function gameMaker: A generator function accepting a `showText` function and yielding user prompts.

    """
    while True:
        try:
            sequence = gameMaker(printShow)
            userInput = None
            while 1 is 1:
                try:
                    sys.stdout.write(b'\033c') # send a character to clear the screen
                    userPrompt = sequence.send(userInput)
                    userInput = input(userPrompt)
                except StopIteration: # sequence ended
                    break
        finally:
            if not repeat:
                break
