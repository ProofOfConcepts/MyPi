#!usr/bin/env python  
#coding=utf-8  

from __future__ import print_function

import logging
import argparse
import os.path
import json
import sys
import os 
import subprocess

import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

from conversation import say
from conversation import conversationStarted
from conversation import conversationFinished
from conversation import processCommand
from conversation import playWavFile
from configurations import getconfigs
import constants

dir_path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename=constants.LOG_FILE, level=constants.LOG_LEVEL,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

configData = getconfigs()

DEVICE_API_URL = configData[constants.DEVICE_API_URL_KEY]


def process_device_actions(event, device_id):
    if 'inputs' in event.args:
        for i in event.args['inputs']:
            if i['intent'] == 'action.devices.EXECUTE':
                for c in i['payload']['commands']:
                    for device in c['devices']:
                        if device['id'] == device_id:
                            if 'execution' in c:
                                for e in c['execution']:
                                    if 'params' in e:
                                        yield e['command'], e['params']
                                    else:
                                        yield e['command'], None


def process_event(event, device_id):
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        conversationStarted(dir_path + configData[constants.LISTENING_AUDIO_FILE_KEY])

    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args[constants.EVENT_ARGS_WITH_FOLLOW_ON_TURN]):
        conversationFinished(dir_path + configData[constants.HOTWORD_WAITING_AUDIO_FILE_KEY])
    
    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in process_device_actions(event, device_id):
            processCommand(command, params)


def register_device(project_id, credentials, device_model_id, device_id):
    base_url = '/'.join([DEVICE_API_URL, 'projects', project_id, 'devices'])
    device_url = '/'.join([base_url, device_id])
    session = google.auth.transport.requests.AuthorizedSession(credentials)
    r = session.get(device_url)
    print(device_url, r.status_code)
    if r.status_code == 404:
        print(constants.REGISTERING_MESSAGE)
        r = session.post(base_url, data=json.dumps({
            'id': device_id,
            'model_id': device_model_id,
            'client_type': constants.CLIENT_TYPE
        }))
        if r.status_code != 200:
            raise Exception(constants.REGISTRATION_FAILED_MESSAGE + r.text)
        print(constants.REGISTRATION_DONE_MESSAGE)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(constants.CREDENTIALS_ARG, type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    parser.add_argument(constants.DEVICE_MODEL_ARG, type=str,
                        metavar='DEVICE_MODEL_ID', required=True,
                        help='The device model ID registered with Google')
    parser.add_argument(
        constants.PROJECT_ARG,
        type=str,
        metavar='PROJECT_ID',
        required=False,
        help='The project ID used to register device instances.')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' +
        Assistant.__version_str__())

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials, args.device_model_id) as assistant:
        # Play intro audio
        playWavFile(dir_path + configData[constants.STARTUP_AUDIO_FILE_KEY])
        say(configData[constants.STARTUP_MESSAGE_KEY], configData[constants.SAY_FILE_KEY])
        events = assistant.start()

        print('device_model_id:', args.device_model_id + '\n' +
              'device_id:', assistant.device_id + '\n')

        if args.project_id:
            register_device(args.project_id, credentials,
                            args.device_model_id, assistant.device_id)

        #indicate that we are ready now...
        playWavFile(dir_path + configData[constants.HOTWORD_WAITING_AUDIO_FILE_KEY])
        for event in events:
            process_event(event, assistant.device_id)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        logger.exception(error)