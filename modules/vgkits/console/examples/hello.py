def createHelloGame(show):
    while True:
        show("Welcome to the game")
        username = yield "What is your name? "
        show("Hello " + username)
        yield "Press enter to restart the game "

