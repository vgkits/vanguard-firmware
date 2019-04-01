from time import sleep

def testRoutine(prompt):
    manAdjective = yield "Write an adjective for a man? "
    manName = yield "Write a name for a man? "
    womanAdjective = yield "Write an adjective for a woman? "
    womanName = yield "Write a name for a woman? "
    placeName = yield "Where were they? "
    placeReason = yield "Why were they there? "
    manWearing = yield "What was the man wearing?"
    womanWearing = yield "What was the woman wearing? "
    manSaid = yield "What did the man say? "
    womanSaid = yield "What did the woman say? "
    result = yield "What were the consequences? "
    show (manAdjective + " " + manName + " met " + womanAdjective + " " + womanName + " at " + placeName + " to " + placeReason)
    sleep(0.5)
    show(manName + " wore " + manWearing)
    sleep(0.5)
    show(womanName + " wore " + womanWearing)
    sleep(0.5)
    show(manName + " said " + manSaid)
    sleep(0.5)
    show(womanName + " said " + womanSaid)
    sleep(0.5)
    show("...and the consequences were " + result)
