#!usr/bin/env python  
#coding=utf-8  

from gtts import gTTS
from googletrans import Translator
import os
import subprocess
from jukebox import JukeBoxRequest
import constants

translator = Translator()
language = "en"
myJukeBox = JukeBoxRequest()

def say(words, ttsfilename):
    words= translator.translate(words, dest=language)
    words=words.text
    words=words.replace("Text, ",'',1)
    words=words.strip()
    print(words)
    tts = gTTS(text=words, lang=language)
    tts.save(ttsfilename)
    playMp3File(ttsfilename)
    os.remove(ttsfilename)

def playWavFile(fileName):
    subprocess.Popen(["aplay", fileName], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def playMp3File(fileName):
    os.system("mpg123 " + fileName)

def conversationStarted(listeningFilePath):
    myJukeBox.jukeBoxConversationStarted()
    playWavFile(listeningFilePath)
    print(constants.CONVERSATION_TURN_STARTED_MESSAGE)

def conversationFinished(hotwordWaitingFilePath):
    playWavFile(hotwordWaitingFilePath)
    myJukeBox.jukeBoxConversationFinished()
    print(constants.CONVERSATION_TURN_FINISHED_MESSAGE)

def processCommand(command, params):
    print(constants.DO_COMMAND_MESSAGE, command, constants.WITH_PARAMS_MESSAGE, str(params))
    if command == constants.JUKEBOXES_PLAY_COMMAND:
        myJukeBox.jukeBoxPlayRequest(params["number"], params["locationkey"])
    if command == constants.JUKEBOXES_STOP_COMMAND or command == constants.JUKEBOXES_PAUSE_COMMAND or command == constants.JUKEBOXES_RESUME_COMMAND:
        myJukeBox.jukeBoxOtherRequest(command, params["locationkey"])
    if command == constants.JUKEBOXES_VOLUME_COMMAND:
        print("Adjusting Volume...")
