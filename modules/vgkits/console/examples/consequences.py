from time import sleep

def testRoutine(prompt):
    manAdjective = prompt("Write an adjective for a man? ")
    prompt(None)
    manName = prompt("Write a name for a man? ")
    prompt(None)
    womanAdjective = prompt("Write an adjective for a woman? ")
    prompt(None)
    womanName = prompt("Write a name for a woman? ")
    prompt(None)
    placeName = prompt("Where were they? ")
    prompt(None)
    placeReason = prompt("Why were they there? ")
    prompt(None)
    manWearing = prompt("What was the man wearing?")
    prompt(None)
    womanWearing = prompt("What was the woman wearing? ")
    prompt(None)
    manSaid = prompt("What did the man say? ")
    prompt(None)
    womanSaid = prompt("What did the woman say? ")
    prompt(None)
    result = prompt("What were the consequences? ")
    prompt(None)
    yield manAdjective + " " + manName + " met " + womanAdjective + " " + womanName + " at " + placeName + " to " + placeReason
    sleep(0.5)
    yield manName + " wore " + manWearing
    sleep(0.5)
    yield womanName + " wore " + womanWearing
    sleep(0.5)
    yield manName + " said " + manSaid
    sleep(0.5)
    yield womanName + " said " + womanSaid
    sleep(0.5)
    yield "...and the consequences were " + result
