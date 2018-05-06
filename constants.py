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
JUKEBOXES_PLAYERCONTROLREQUEST_ENDPOINT_KEY = "playercontrolrequestendpoint"
JUKEBOXES_CONVERSATION_START_ENDPOINT_KEY = "conversationstartedendpoint"
JUKEBOXES_CONVERSATION_END_ENDPOINT_KEY = "conversationfinishedendpoint"
JUKEBOXES_PLAY_COMMAND = "com.mypi.commands.play_jukebox"
JUKEBOXES_PAUSE_COMMAND = "com.mypi.commands.pause_jukebox"
JUKEBOXES_RESUME_COMMAND = "com.mypi.commands.resume_jukebox"
JUKEBOXES_STOP_COMMAND = "com.mypi.commands.stop_jukebox"
JUKEBOXES_VOLUME_COMMAND = "com.mypi.commands.jukebox_volume"
JUKEBOXES_VOLUMEUP_OPERATION = "increase"
JUKEBOXES_VOLUMEDOWN_OPERATION = "decrease"
JUKEBOXES_SMALL_STEP = "small"
JUKEBOXES_LARGE_STEP = "large"
JUKEBOXES_MAX_STEP = "max"
JUKEBOXES_MIN_STEP = "min"
JUKEBOXES_VOLUME_SMALL_STEP = 5
JUKEBOXES_VOLUME_LARGE_STEP = 10


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
