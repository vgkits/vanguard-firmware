from time import sleep

def testRoutine(prompt):
    username = prompt("What is your name? ")
    yield username + " is cool"    
