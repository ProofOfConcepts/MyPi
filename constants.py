#!usr/bin/env python  
#coding=utf-8  

import logging

LOG_FILE = "/tmp/MyPi.log"
LOG_LEVEL = logging.DEBUG

DEVICE_API_URL_KEY = "deviceapiurl"
STARTUP_MESSAGE_KEY = "startupmessage"
LISTENING_AUDIO_FILE_KEY = "listeningaudiofile"
HOTWORD_WAITING_AUDIO_FILE_KEY = "hotwordwaitingaudiofile"
STARTUP_AUDIO_FILE_KEY = "startupaudiofile"
SAY_FILE_KEY = "sayfilename"

JUKEBOXES_KEY = "jukeboxes"
JUKEBOXES_NAMES_KEY = "name"
JUKEBOXES_ISDEFAULT_KEY = "isdefault"
JUKEBOXES_HOST_KEY = "host"
JUKEBOXES_PLAYERREQUEST_ENDPOINT_KEY = "playerrequestendpoint"


CONVERSATION_TURN_STARTED_MESSAGE = "I am here..."
CONVERSATION_TURN_FINISHED_MESSAGE = "Finished.\nWaiting for hotword..."
DO_COMMAND_MESSAGE = "Do command"
WITH_PARAMS_MESSAGE = 'with params'
REGISTERING_MESSAGE = 'Registering....'
REGISTRATION_FAILED_MESSAGE = 'failed to register device: '
REGISTRATION_DONE_MESSAGE = '\rDevice registered.'
CONFIG_FILE_READ_FAIL_MESSAGE = "There was an error reading configuration file\n"
CONFIG_FILE_READ_PATH_MESSAGE = "Trying to read config file: "


EVENT_ARGS_WITH_FOLLOW_ON_TURN = "with_follow_on_turn"

CLIENT_TYPE = 'SDK_LIBRARY'

CREDENTIALS_ARG = '--credentials'
DEVICE_MODEL_ARG = '--device_model_id'
PROJECT_ARG = '--project_id'
