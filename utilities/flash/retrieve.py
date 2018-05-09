import os
import requests

from config import retrievalConfig

def get_firmware():
    retrievalLookup = retrievalConfig()
    # retrieve from url, write to local path
    remote_url = retrievalLookup["remote_image_url"]
    local_path = retrievalLookup["local_image_path"]
    if not (os.path.isfile(local_path)):
        print("Retrieving Micropython Image")
        r = requests.get(remote_url, stream=True)
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    else:
        print("Micropython image already retrieved")
    return local_path


def run():
    get_firmware()


if __name__ == "__main__":
    run()
