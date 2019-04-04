
#from vgkits.console.gameConsole import hostGame
from vgkits.console.webGameConsole import hostGame

#from vgkits.console.examples.hangman import createHangmanGame as createGame
#from vgkits.console.examples.hello import createHelloGame as createGame
from vgkits.console.examples.chatroom import createChatGame as createGame
from vgkits.console.examples.mathdice import diceRoutine as createGame

hostGame(createGame)