
from vgkits.random import randint

operators = "+-*x/"    


def getRandomTarget():
    return randint(87) + 13


def getRandomDice():
    numDice = 3
    numSides = 6
    s = set()
    while len(s) < numDice:
        s.add(randint(numSides) + 1)
    return s


def getRandomItem(collection):
    l = list(collection)
    return l[randint(len(l))]

        
def calculateNewNumber(numberSet, calculation):
    for operator in operators:
        if operator in calculation:
            before, after = calculation.split(operator)
            numberBefore, numberAfter = int(before),int(after)
            if numberBefore not in numberSet or numberAfter not in numberSet:
                raise Exception("No cheating!")
            if operator is "+":
                result = numberBefore + numberAfter
            elif operator is "-":
                result = numberBefore - numberAfter
            elif operator is "*" or operator is "x":
                result = numberBefore * numberAfter
            elif operator is "/":
                result = numberBefore // numberAfter
            numberSet.add(result)
            return result, "%d %s %d = %d" % (numberBefore, operator, numberAfter, result)
    else:
        raise Exception("'%s' isn't a two figure sum?" % calculation)
    
        
def createSequence(print):
    import gc
    name = yield "What is your name?\n"
    while True:
        turn = 0
        numbers = getRandomDice()
        target = getRandomTarget()
        result = None
        while result is not target:
            numberSequence = sorted(list(numbers))
            try:
                turn = turn + 1
                calculation = yield "Turn %d: Enter a sum using %s to get closer to %d \n" % (turn, numberSequence, target)
                result, working = calculateNewNumber(numbers, calculation)
                print(working)
                if result is target:
                    break
            except Exception as e:
                print(str(e))
                print("Type a sum like %d %s %d" % (getRandomItem(numberSequence), getRandomItem(operators), getRandomItem(numberSequence)))
        print("Well done, %s, you reached %d in %d turns!" % (name, target, turn))
        gc.collect()
