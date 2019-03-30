from time import sleep

def helloRoutine(prompt):
    while True:
        name = prompt("What is your name? ")
        if "poo" in name:
            yield "That's rude, try again"
            continue
        sleep(1)
        yield "Hello, " + name
        sleep(1)
        yield "I hope you are having a great day today!"
        sleep(4)
        yield "\n"
        prompt(None) # clears the screen
