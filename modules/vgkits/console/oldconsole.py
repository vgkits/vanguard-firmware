import sys
def _createAnswerGenerator():
    """
        Creates a generator of answers typed in response to questions. 
        Once the loop is primed you can use gen.send('My text prompt') 
        to receive a typed answer to a text prompt you send 
    """
    nextQuestion = None # no question known first time round 
    while True:
        if nextQuestion is not None:    # prompt() sent a question last time round
            response = input(nextQuestion)
        else:
            clearScreen()               # reset the screen
            response = None             # no question was sent, can't get a response
        nextQuestion = yield response   # try and get a question sent by prompt()  


def makePrompt():
    """ 
        Returns a prompt() function that you can use to prompt the user to type 
        an answer to your question through the console as part of a game.
        For example:
        username = prompt("What is your name?")
    """
    answerGenerator = _createAnswerGenerator() # start receiving inputs typed by the user
    next(answerGenerator) # primt the loop (ignoring 1st (empty) user answer) 
    def prompt(question):
        return answerGenerator.send(question)
    return prompt


def clearScreen():
    sys.stdout.write(b'\033c')  # clears the screen in most VT100 terminals

    
def printLines(lines):
    """
        Calls print() for each item of text returned by 'lines'
        causing the text to appear in the console
    """
    for line in lines:
        print(line)

        
def runGame(makeGame):
    """
        Sets up a prompt() function to get input from a user.
        Calls the provided makeGame function, giving it a reference to the prompt.
        Then outputs all the lines yielded from the makeGame function until it returns
    """
    clearScreen()
    prompt = makePrompt()
    game = makeGame(prompt)
    printLines(game)
