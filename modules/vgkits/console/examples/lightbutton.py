senderBytes = b"""
  <script>
    function sendValue(value){
      xhr = new XMLHttpRequest()
      xhr.open("POST", window.location, true);
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      xhr.send("response=" + value);
    }
  </script>
"""

buttonBytes = b"""<button onmousedown="sendValue('on')" onmouseup="sendValue('off')" >Label</button>"""

def setLight(value):
  if value:
    print("Light is On")
  else:
    print("Light is Off")

def createSequence(print):
  print(senderBytes)
  print(buttonBytes)
  response = yield
  if response == 'on':
    setLight(True)
  elif response == 'off':
    setLight(False)
  else:
    print("Unexpected response")


def run():
  from vgkits.console.webGameConsole import hostGame
  hostGame(createSequence, repeat=True, debug=False)


if __name__ == "__main__":
  run()