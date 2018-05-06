#!usr/bin/env python  
#coding=utf-8  

from gtts import gTTS
from google.assistant.library import Assistant
from googletrans import Translator
import os
import subprocess

translator = Translator()
language = "en"

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

def sayAssistant(assistant, text):
    text_to_speech = '<speak>' + text + '<audio src="https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg">a digital watch alarm</audio>.</speak>'
    assistant.tell(text_to_speech)

def playWavFile(fileName):
    subprocess.Popen(["aplay", fileName], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def playMp3File(fileName):
    os.system("mpg123 " + fileName)