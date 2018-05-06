#!usr/bin/env python  
#coding=utf-8  

from gtts import gTTS
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

def playWavFile(fileName):
    subprocess.Popen(["aplay", fileName], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def playMp3File(fileName):
    os.system("mpg123 " + fileName)

def conversationStarted():
    