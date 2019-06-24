from gtts import gTTS
import speech_recognition as sr
import os
import webbrowser
import smtplib
import pyttsx3
from pygame import mixer

count = 0

def talkToMe(audio):
    global count
    print(audio)
    text_to_speech = gTTS(text=audio, lang='vi')
    text_to_speech.save(f'{count%2}.mp3')
    mixer.init()
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
        command = r.recognize_google(audio)
        print('You said ' + command + '/n')

    #loop back to continue listening for commands

    except sr.UnknownValueError:
        print('Could not hear')
        command = myCommand();

    return command

#if statement for executing command

def assistant(command):

    if 'open Facebook' in command:
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        url = 'https://www.facebook.com/'
        webbrowser.get(chrome_path).open(url)

    if 'hello' in command:
         talkToMe('Chào')

talkToMe('Sẵn sàng')

while True:
    assistant(myCommand())
        

    
