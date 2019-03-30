def manLines(stage):
    # head line
    if stage < 1:
        return      # don't draw anything
    else:
        yield " O"      # draw head
    # torso line
    if stage < 2 :
        return              # finished
    else:
        if stage < 3:
            yield "/"       # draw one arm 
        elif stage < 4:
            yield "/ \\"    # draw two arms
        else:
            yield "/|\\"    # draw two arms and torso
    # hips line
    if stage < 5:
        return          # finished
    else:
        yield " |"      # draw hips
    # legs line
    if stage < 6:
        return
    else:
        if stage < 7:
            yield "/"       # one leg
        else:
            yield "/ \\"    # both legs

def gallowsLines(stage):
    padding = "|    "
    yield "_______"
    yield padding + " |"
    remaining = 5
    for line in manLines(stage): # DRAW ENOUGH MAN FOR THIS STAGE
        yield padding + line
        remaining = remaining - 1
    for count in range(0, remaining): # EMPTY SPACE BELOW
        yield padding
    yield "|-------"
    
def showWord(word, guesses):
    letters = []
    for letter in word:
        if letter is " " or letter in guesses:
            letters.append(letter)
        else:
            letters.append("_")
    return "".join(letters)


def hangmanRoutine(prompt):
    word = ""
    while word == "":
        word = prompt("Enter an english word or phrase: ")
        for letter in word:
            if letter.isalpha():
                continue
            elif letter == " ":
                continue
            else:
                word = ""
                yield "You can only use letters or spaces"
                break
    word = word.lower() # force input to lowercase
    prompt(None) # clear screen
    guessed = ""
    stage = 0
    yield from gallowsLines(stage)
    yield ""
    yield "Guess letters from the word or phrase below"
    yield ""
    while True:
        masked = showWord(word, guessed)
        if masked == word:
            yield "You won!"
            yield ""
            yield "The answer was '" + word + "'"
            yield ""
            return prompt(" Press enter to reset")
        else:
            yield " ".join(list(masked))
            yield ""
            typed = prompt("Type a letter and press enter: ")
            typed = typed.lower() # force input to lowercase
            if len(typed) == 0:
                yield "You didn't type anything"
                continue
            elif len(typed) > 1:
                yield "You can't type more than one letter"
                continue
            elif typed in guessed:
                yield "You already guessed " + typed
                continue
            else:
                prompt(None) # clear screen
                guessed = guessed + typed
                if typed in word:
                    yield from gallowsLines(stage)
                    yield ""
                    yield "Great! The word contains " + typed
                    yield ""
                    continue
                else :
                    stage = stage + 1
                    yield from gallowsLines(stage)
                    yield ""
                    yield "Oh no! The word doesn't contain " + typed
                    yield ""
                if stage == 7:
                    yield "You used up all your chances and got hung!"
                    yield "The word was '" + word + "'"
                    return prompt("You lost! Press enter to reset")
