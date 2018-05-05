import json
import os
def getconfigs():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
    print("trying to open file: " + file_path)
    with open(file_path) as file:
        message = "Welcome, If you need me just say Hello Google or Hey Google"
        sayfilename = "/tmp/words.mp3"
        startupaudiofile = "/assets/startup.wav"
        listeningaudiofile = "/assets/listening.wav"
        data = {"startupmessage" : message, "sayfilename" : sayfilename, "startupaudiofile" : startupaudiofile, "listeningaudiofile" : listeningaudiofile}
        try:
            data = json.load(file)
        except Exception as error:
            print("There was an error reading configuration file\n" + error)
        return data

def main():
    print(getconfigs())

if __name__ == '__main__':
    main()