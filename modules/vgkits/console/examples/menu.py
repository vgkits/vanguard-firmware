names = ("Hangman", "Math Dice", "Consequences", "Chat")

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
    if choice == "hangman":
        from vgkits.console.examples import hangman
        yield from hangman.createSequence(print)
    elif choice == "mathdice":
        from vgkits.console.examples import mathdice
        yield from mathdice.createSequence(print)
    elif choice == "consequences":
        from vgkits.console.examples import consequences
        yield from consequences.createSequence(print)
    elif choice == "chat":
        from vgkits.console.examples import chat
        yield from chat.createSequence(print)

if __name__ == "__main__":
    from vgkits.console.webGameConsole import hostGame
    hostGame(createSequence)