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
                print("host found...\nProcessing on host: " + host)
                url= jukebox["host"] + self.data[constants.JUKEBOXES_PLAYERREQUEST_ENDPOINT_KEY]
                if requestType == constants.JUKEBOXES_STOP_COMMAND:
                    data = self.getPlayerRequestData(2, -1)
                    self.postData(url, data)
                if requestType == constants.JUKEBOXES_PAUSE_COMMAND:
                    data = self.getPlayerRequestData(1, -1)
                    self.postData(url, data)
                if requestType == constants.JUKEBOXES_RESUME_COMMAND:
                    data = self.getPlayerRequestData(3, -1)
                    self.postData(url,data)


    def jukeBoxConversationStarted(self):
        for jukebox in self.data["jukeboxes"]:
            try:
                url = jukebox["host"] + self.data[constants.JUKEBOXES_CONVERSATION_START_ENDPOINT_KEY]
                self.getData(url)
            except:
                print("jukeBoxConversationStarted: Looks like {0} is not available...".format(jukebox["host"]))

    def jukeBoxConversationFinished(self):
        for jukebox in self.data["jukeboxes"]:
            try:
                url = jukebox["host"] + self.data[constants.JUKEBOXES_CONVERSATION_END_ENDPOINT_KEY]
                self.getData(url)
            except:
                print("jukeBoxConversationFinished: Looks like {0} is not available...".format(jukebox["host"]))

    def jukeboxVolumeRequest(self, amount, operation, host):
        for jukebox in self.data["jukeboxes"]:
            if jukebox["name"] == host:
                print("host found...\nProcessing volume on host: " + host)
                url= jukebox["host"] + self.data[constants.JUKEBOXES_PLAYERCONTROLREQUEST_ENDPOINT_KEY]
                step = 0
                if amount == constants.JUKEBOXES_SMALL_STEP:
                    step = 5
                if amount == constants.JUKEBOXES_LARGE_STEP:
                    step = 10
                if amount == constants.JUKEBOXES_MAX_STEP:
                    step = 100
                if amount == constants.JUKEBOXES_MIN_STEP:
                    step = 0
                if operation == constants.JUKEBOXES_VOLUMEDOWN_OPERATION:
                    step = step * -1
                data = self.getPlayerControlRequestData(5, step)
                print("sending data:\n" + str(data))
                response = self.postData(url, data)
                print(response)
    
    def getPlayerControlRequestData(self, requestType, requestParam):
        data = {
            "controlRequest": requestType,
            "requestData": requestParam
        }
        return data

    def playSong(self, songNumber, url):
        data = self.getPlayerRequestData(0, songNumber)
        self.postData(url, data)

    def getPlayerRequestData(self, requestType, identifier):
        data = {
            "RequestType":requestType,
            "Identifier":identifier
        }
        return data

    def getData(self, url):
        print("getting from: " + url)
        headers = {"Content-Type" : "application/json"}
        response = requests.get(url, headers=headers)
        print(response.text)
        return response.text

    def postData(self, url, data):
        print("posting to: " + url)
        headers = {"Content-Type" : "application/json"}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(response.text)
        return response.text

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