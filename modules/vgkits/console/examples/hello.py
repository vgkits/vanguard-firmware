def createHelloGame(print):
    print("Welcome to the game")
    username = yield "What is your name? "
    print("Hello " + username)
    yield "Press enter to restart the game "
