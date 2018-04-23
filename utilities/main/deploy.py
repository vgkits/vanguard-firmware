from config import mainPath
from command import putFile

def run():
    if mainPath is not None:
        print("Deploying main.py file")
        putFile(mainPath, "main.py")

if __name__ == "__main__":
    run()