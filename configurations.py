#!usr/bin/env python  
#coding=utf-8  

import json
import os
import constants

def getconfigs():
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
    print(constants.CONFIG_FILE_READ_PATH_MESSAGE + file_path)
    with open(file_path) as file:
        #initialize with default values
        data = {
            constants.STARTUP_MESSAGE_KEY : "Welcome, If you need me just say Hello Google or Hey Google",
            constants.SAY_FILE_KEY : "/tmp/words.mp3",
            constants.STARTUP_AUDIO_FILE_KEY : "/assets/startup.wav",
            constants.LISTENING_AUDIO_FILE_KEY : "/assets/listening.wav",
            constants.HOTWORD_WAITING_AUDIO_FILE_KEY : "/assets/waiting-hotword.wav",
            constants.DEVICE_API_URL_KEY : "https://embeddedassistant.googleapis.com/v1alpha2"
            }
        try:
            data = json.load(file)
        except Exception as error:
            print(constants.CONFIG_FILE_READ_FAIL_MESSAGE + error)
        return data

def main():
    print(getconfigs())

if __name__ == '__main__':
    main()