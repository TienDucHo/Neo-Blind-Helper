from gtts import gTTS
import speech_recognition as sr
import os
import webbrowser
import smtplib
from pygame import mixer

count = 0

mixer.init()

def talkToMe(audio):
    global count
    print(audio)
    text_to_speech = gTTS(text=audio, lang='vi')
    text_to_speech.save(f'{count%2}.mp3')

    mixer.music.load(f'{count%2}.mp3')
    mixer.music.play()
    count += 1

#listen for commands

def myCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('I am ready for your command')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language='vi-VI')
        print('You said ' + command + '/n')

    #loop back to continue listening for commands

    except sr.UnknownValueError:
        print('Could not hear')
        command = myCommand();

    return command

#if statement for executing command

def assistant(command):

    if 'Mở Facebook' in command:
        chrome_path = ''
        url = 'https://www.facebook.com/'
        webbrowser.open(url)

    if 'Chào bạn' in command:
         talkToMe('Chào')

talkToMe("Hello Mr. Pussy Face")

while True:
    assistant(myCommand())
