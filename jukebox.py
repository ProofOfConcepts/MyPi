#!usr/bin/env python  
#coding=utf-8  

import requests
import json
import os
import constants

class JukeBoxRequest:

    def handleJukeBoxRequest(self, songnumber, host):
        print("song number: " + songnumber + " , location: " + host)
        for jukebox in self.data["jukeboxes"]:
            if jukebox["name"] == host:
                print("host found...\nplaying song on host: " + host)
                self.playSong(songnumber, url= jukebox["host"] + self.data["playerrequestendpoint"])

    def playSong(self, songNumber, url):
        data = '''
            {
	            "RequestType": 0,
	            "Identifier": ''' + songNumber
        '''}'''
        response = requests.post(url, data=data)
        print(str(response))

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