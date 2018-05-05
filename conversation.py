#!/usr/bin/env python

from gtts import gTTS
from googletrans import Translator
import os

translator = Translator()
language = "en"
speechfilename = "/tmp/words.mp3"

def say(words, ttsfilename):
    words= translator.translate(words, dest=language)
    words=words.text
    words=words.replace("Text, ",'',1)
    words=words.strip()
    print(words)
    tts = gTTS(text=words, lang=language)
    tts.save(ttsfilename)
    os.system("mpg123 "+ttsfilename)
    os.remove(ttsfilename)