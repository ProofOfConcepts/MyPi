#!usr/bin/env python  
#coding=utf-8  

from __future__ import print_function

import logging
import argparse
import os.path
import json
import pyaudio  
import wave  
import sys
import os 
import subprocess

import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

from conversation import say
from configurations import getwelcomemessage


DEVICE_API_URL = 'https://embeddedassistant.googleapis.com/v1alpha2'

CHUNK_SIZE = 1024

dir_path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename='/tmp/MyPi.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

welcomemessage = getwelcomemessage

def play_wav(wav_filename, chunk_size=CHUNK_SIZE):
    '''
    Play (on the attached system sound device) the WAV file
    named wav_filename.
    '''

    try:
        print('Welcome...\nNow starting the assistant')
        wf = wave.open(wav_filename, 'rb')
    except IOError as ioe:
        sys.stderr.write('IOError on file ' + wav_filename + '\n' + \
        str(ioe) + '. Skipping.\n')
        return
    except EOFError as eofe:
        sys.stderr.write('EOFError on file ' + wav_filename + '\n' + \
        str(eofe) + '. Skipping.\n')
        return

    # Instantiate PyAudio.
    p = pyaudio.PyAudio()

    # Open stream.
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk_size)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop stream.
    stream.stop_stream()
    stream.close()

    # Close PyAudio.
    p.terminate()

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
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
        device_id(str): The device ID of the new instance.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print()

    print(event)

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print()
    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in process_device_actions(event, device_id):
            print('Do command', command, 'with params', str(params))


def register_device(project_id, credentials, device_model_id, device_id):
    """Register the device if needed.

    Registers a new assistant device if an instance with the given id
    does not already exists for this model.

    Args:
       project_id(str): The project ID used to register device instance.
       credentials(google.oauth2.credentials.Credentials): The Google
                OAuth2 credentials of the user to associate the device
                instance with.
       device_model_id(str): The registered device model ID.
       device_id(str): The device ID of the new instance.
    """
    base_url = '/'.join([DEVICE_API_URL, 'projects', project_id, 'devices'])
    device_url = '/'.join([base_url, device_id])
    session = google.auth.transport.requests.AuthorizedSession(credentials)
    r = session.get(device_url)
    print(device_url, r.status_code)
    if r.status_code == 404:
        print('Registering....')
        r = session.post(base_url, data=json.dumps({
            'id': device_id,
            'model_id': device_model_id,
            'client_type': 'SDK_LIBRARY'
        }))
        if r.status_code != 200:
            raise Exception('failed to register device: ' + r.text)
        print('\rDevice registered.')


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    parser.add_argument('--device_model_id', type=str,
                        metavar='DEVICE_MODEL_ID', required=True,
                        help='The device model ID registered with Google')
    parser.add_argument(
        '--project_id',
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
        subprocess.Popen(["aplay", dir_path + "/assets/startup.wav"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        say("", "/tmp/words.mp3")
        events = assistant.start()

        print('device_model_id:', args.device_model_id + '\n' +
              'device_id:', assistant.device_id + '\n')

        if args.project_id:
            register_device(args.project_id, credentials,
                            args.device_model_id, assistant.device_id)

        for event in events:
            process_event(event, assistant.device_id)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        logger.exception(error)