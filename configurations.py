import json
import os
def getwelcomemessage():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
    with open(file_path) as file:
        try:
            return json.load(file)["startupmessage"]
        except Exception as error:
            print("There was an error reading configuration file\n" + error)
            return "Welcome, If you need me just say Hello Google or Hey Google"