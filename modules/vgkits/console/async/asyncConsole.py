import sys
if sys.implementation.name == "micropython":
    import uasyncio as asyncio
else:
    import asyncio


async def asyncPrompt(msg):
    return input(msg)


async def asyncShow(line):
    print(line)    

    
async def createHelloSequence(show, prompt):
    name = await prompt("What is your name? ")
    await show("Hello %s" % name)


def hostSequence(sequenceFactory, asyncShow=asyncShow, asyncPrompt=asyncPrompt):
    loop = asyncio.get_event_loop()
    sequence = sequenceFactory(asyncShow, asyncPrompt)
    try:
        loop.run_until_complete(sequence)
    except KeyboardInterrupt:
        print('Interrupted')

def run():
    hostSequence(createHelloSequence)
