names = ("Hello World", "Hangman", "Math Dice", "Consequences", "Chat")

lastChoice = None

def createSequence(print):
    global lastChoice
    print("The following games are available:")
    for name in names:
        print(name)

    if lastChoice is None:
        choice = yield "Type the game you want to run"
    else:
        choice = yield "Type the game you want to run" + " or press Enter to run " + lastChoice
        if choice == "":
            choice = lastChoice

    lastChoice = choice
    choice = choice.lower()             # make lowercase
    choice = choice.replace(" ", "")    # remove spaces

    if choice == "helloworld":
        from vgkits.console.examples.helloworld import createSequence
    if choice == "hangman":
        from vgkits.console.examples.hangman import createSequence
    elif choice == "mathdice":
        from vgkits.console.examples.mathdice import createSequence
    elif choice == "consequences":
        from vgkits.console.examples.consequences import createSequence
    elif choice == "chat":
        from vgkits.console.examples.chat import createSequence

    sequence = createSequence(print)
    yield from sequence

if __name__ == "__main__":
    from vgkits.console.webGameConsole import hostGame
    hostGame(createSequence)