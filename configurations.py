import json
import os
def getwelcomemessage():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
    print("trying to open file: " + file_path)
    with open(file_path) as file:
        try:
            data = json.load(file)
            message = data["startupmessage"]
            print("Startup Message: " + message)
        except Exception as error:
            print("There was an error reading configuration file\n" + error)
            return "Welcome, If you need me just say Hello Google or Hey Google"

def main():
    print(getwelcomemessage())

if __name__ == '__main__':
    main()