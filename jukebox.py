#!usr/bin/env python  
#coding=utf-8  

import requests
import json
import os
import constants

class JukeBoxRequest:

    def jukeBoxPlayRequest(self, songnumber, host):
        print("song number: " + songnumber + " , location: " + host)
        for jukebox in self.data["jukeboxes"]:
            if jukebox["name"] == host:
                print("host found...\nplaying song on host: " + host)
                self.playSong(songnumber, url= jukebox["host"] + self.data["playerrequestendpoint"])

    def jukeBoxOtherRequest(self, requestType, host):
        for jukebox in self.data["jukeboxes"]:
            if jukebox["name"] == host:
                print("host found...\nstopping on host: " + host)
                url= jukebox["host"] + self.data["playerrequestendpoint"]
                if requestType == "com.acme.commands.stop_jukebox":
                    data = self.getPlayerRequestData(2, -1)
                    self.postData(url, data)
    
    def postData(self, url, data):
        print("posting to: " + url)
        headers = {"Content-Type" : "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(response)

    def playSong(self, songNumber, url):
        data = self.getPlayerRequestData(0, songNumber)
        self.postData(url, data)

    def getPlayerRequestData(self, requestType, identifier):
        data = {
            "RequestType":requestType,
            "Identifier":identifier
        }
        return data
    def __init__(self):
        file_path = os.path.dirname(os.path.realpath(__file__)) + "/jukebox-config.json"
        print(constants.CONFIG_FILE_READ_PATH_MESSAGE + file_path)
        with open(file_path) as file:
            data = {
                constants.JUKEBOXES_KEY : [
                    {
                        constants.JUKEBOXES_NAMES_KEY : "zero",
                        constants.JUKEBOXES_ISDEFAULT_KEY : True,
                        constants.JUKEBOXES_HOST_KEY : "http://192.168.1.201:5000"
                    },
                    {
                        constants.JUKEBOXES_NAMES_KEY : "one",
                        constants.JUKEBOXES_ISDEFAULT_KEY : True,
                        constants.JUKEBOXES_HOST_KEY : "http://192.168.1.200:5000"
                    }
                ],
                constants.JUKEBOXES_PLAYERREQUEST_ENDPOINT_KEY : "/api/Player/Request"
            }
            try:
                data = json.load(file)
            except Exception as error:
                print(constants.CONFIG_FILE_READ_FAIL_MESSAGE + error)
            self.data =  data