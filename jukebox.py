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
                self.playSong(songnumber, url= jukebox["host"] + self.data[constants.JUKEBOXES_PLAYERREQUEST_ENDPOINT_KEY])

    def jukeBoxOtherRequest(self, requestType, host):
        for jukebox in self.data["jukeboxes"]:
            if jukebox["name"] == host:
                print("host found...\nstopping on host: " + host)
                url= jukebox["host"] + self.data[constants.JUKEBOXES_PLAYERREQUEST_ENDPOINT_KEY]
                if requestType == "com.acme.commands.stop_jukebox":
                    data = self.getPlayerRequestData(2, -1)
                    self.postData(url, data)
                if requestType == "com.acme.commands.pause_jukebox":
                    data = self.getPlayerRequestData(1, -1)
                    self.postData(url, data)
                if requestType == "com.acme.commands.resume_jukebox":
                    data = self.getPlayerRequestData(3, -1)
                    self.postData(url,data)
    
    def jukeBoxConversationStarted(self):
        for jukebox in self.data["jukeboxes"]:
            url = jukebox["host"] + self.data[constants.JUKEBOXES_CONVERSATION_START_ENDPOINT_KEY]
            self.getData(url)

    def jukeBoxConversationFinished(self):
        for jukebox in self.data["jukeboxes"]:
            url = jukebox["host"] + self.data[constants.JUKEBOXES_CONVERSATION_END_ENDPOINT_KEY]
            self.getData(url)

    def getData(self, url):
        print("getting from: " + url)
        headers = {"Content-Type" : "application/json"}
        response = json.load(requests.get(url, headers=headers))
        print(response)
        return response

    def postData(self, url, data):
        print("posting to: " + url)
        headers = {"Content-Type" : "application/json"}
        response = json.load(requests.post(url, data=json.dumps(data), headers=headers))
        print(response)
        return response

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
                constants.JUKEBOXES_PLAYERREQUEST_ENDPOINT_KEY : "/api/Player/Request",
                constants.JUKEBOXES_CONVERSATION_START_ENDPOINT_KEY : "/api/Player/ConversationStarted",
                constants.JUKEBOXES_CONVERSATION_END_ENDPOINT_KEY : "/api/Player/ConversationFinished"
            }
            try:
                data = json.load(file)
            except Exception as error:
                print(constants.CONFIG_FILE_READ_FAIL_MESSAGE + error)
            self.data =  data