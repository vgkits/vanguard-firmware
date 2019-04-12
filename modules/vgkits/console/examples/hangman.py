phraseList = (
    "it's raining cats and dogs",
    "speak of the devil",
    "the best of both worlds",
    "see eye to eye",
    "when pigs fly",
    "costs an arm and a leg",
    "once in a blue moon",
    "a piece of cake",
    "let the cat out of the bag",
    "feeling under the weather",
    "kill two birds with one stone",
    "A bird in the hand is worth two in the bush",
    "A change is as good as a rest",
    "A fish out of water",
    "A friend in need is a friend indeed",
    "A journey of a thousand miles begins with a single step",
    "A leopard cannot change its spots",
    "A watched pot never boils",
    "Curiosity killed the cat",
    "A cat may look at a king",
    "Raining cats and dogs",
    "Let the cat out of the bag",
    "No room to swing a cat",
    "The cats pyjamas",
    "Beauty is in the eye of the beholder",
    "Better to have loved and lost than never to have loved at all",
    "Birds of a feather flock together",
    "Butter wouldn't melt in his mouth",
    "Children should be seen and not heard",
    "The darkest hour is just before the dawn",
)

def manLines(parts):
    """
    Yields from 0 to 4 lines of a 'hangman' stick man. ::
           O
          /|\
           |
          / \

    :param parts: the number of body parts to show from 0 to 7
    :return:
    """
    # head line
    if parts < 1:
        return      # don't draw anything
    else:
        yield " O"      # draw head
    # torso line
    if parts < 2 :
        return              # finished
    else:
        if parts < 3:
            yield "/"       # draw one arm 
        elif parts < 4:
            yield "/ \\"    # draw two arms
        else:
            yield "/|\\"    # draw two arms and torso
    # hips line
    if parts < 5:
        return          # finished
    else:
        yield " |"      # draw hips
    # legs line
    if parts < 6:
        return
    else:
        if parts < 7:
            yield "/"       # one leg
        else:
            yield "/ \\"    # both legs


def gallowsLines(parts):
    """Yields a gallows, with a 'hangman' stick man showing the specified number of body parts. ::

        ________
        |       |
        |       |
        |       O
        |      /|\
        |       |
        |      / \
        |
        |
        |------------

    :param parts:
    :return:
    """
    yield "_______"
    padding = "|    "
    yield padding + " |"
    remaining = 5
    for line in manLines(parts): # DRAW MAN FOR THIS STAGE
        yield padding + line
        remaining = remaining - 1
    for count in range(0, remaining): # FILL REMAINING SPACE
        yield padding
    yield "|-------"


def maskPhrase(phrase, guesses):
    letters = []
    for letter in phrase:
        if letter is " " or letter in guesses:
            letters.append(letter)
        else:
            letters.append("_")
    return "".join(letters)


def createHangmanGame(show):
    phrase = None

    while phrase is None:
        phrase = yield "Enter a word or phrase (leave blank for the computer to choose): "

        if phrase == "": # choose one at random
            from vgkits.random import randint
            phrase = phraseList[randint(len(phraseList))]
        else: # check the user-supplied phrase
            for letter in phrase:
                if letter.isalpha():
                    continue
                elif letter == " ":
                    continue
                else:
                    phrase = None
                    show("You can only use letters or spaces")
                    break

    phrase = phrase.lower() # force input to lowercase
    guessed = ""
    stage = 0
    show("Guess a letter from the word or phrase below")
    show("")
    while True:
        for gallowsLine in gallowsLines(stage):
            show(gallowsLine)
        show("")
        masked = maskPhrase(phrase, guessed)
        if masked == phrase:
            show("You won!")
            show("")
            show("The answer was '" + phrase + "'")
            show("")
            yield "Press enter to reset"
            return
        else:
            show("")
            show(" ".join(list(masked))) # get the characters, put spaces between
            show("")
            typed = yield "Type a letter and press enter: "
            typed = typed.lower() # force input to lowercase
            if len(typed) == 0:
                show("You didn't type a letter!")
                continue
            elif len(typed) > 1:
                show("You can't type more than one letter!")
                continue
            elif typed in guessed:
                show("You already guessed " + typed + "!")
                continue
            else:
                guessed = guessed + typed
                if typed in phrase:
                    show("Great! It contains " + typed)
                    continue
                else:
                    stage = stage + 1
                    show("Oh no! It doesn't contain " + typed)
                    show("")
                if stage == 7:
                    show("You used up all your chances and got hung!")
                    show("The phrase was '" + phrase + "'")
                    yield "You lost! Press enter to reset"
                    return
