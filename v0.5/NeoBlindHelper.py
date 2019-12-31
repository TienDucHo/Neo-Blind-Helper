import os, os.path
import random
import sys
import time

import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

import Command
import GetCategory
import HTMLDom

mixer.init(buffer=1024)
count = 0
url = ""
resume_status = False
response_folder = "response"


def resume():
    global resume_status
    if resume_status:
        playresponse("resume")
        resume_status = False
        mixer.music.unpause()


def talkTitle(audio):
    global count
    tts = gTTS(text = audio, lang = 'vi')
    tts.save("{}.mp3".format(count))
    count = (count + 1) % 2


def talkToMe(audio, name):
    tts = gTTS(text=audio, lang='vi')
    tts.save("{}.mp3".format(name))


def playmp3(addr):
    mixer.music.load(addr)
    mixer.music.play()
    while mixer.music.get_busy():
        continue


def playresponse(response_type):
    folder = "{}\{}".format(response_folder, response_type)
    numoffile = len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])
    file = "{}\{}{:02}.mp3".format(folder, response_type, random.randint(1, numoffile))
    mixer.music.load(file)
    mixer.music.play()
    while mixer.music.get_busy():
        continue


def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Vui lòng nhập lệnh')
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='vi-VI')
        print('Lệnh là ' + command)
    # loop back to continue listening for commands
    except sr.UnknownValueError:
        playresponse("error")
        command = myCommand()
    return command.casefold()


def listenForCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Đợi lệnh')
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='vi-VI')
        print('Lệnh là ' + command)
    # loop back to continue listening for commands
    except sr.UnknownValueError:
        command = ""
    return command.casefold()


def readNews():
    playresponse("page")
    url = ''
    rawCommand = myCommand()
    while url == '':
        for x in GetCategory.supported_page:
            if x in rawCommand:
                url += GetCategory.supported_page[x]
        if url == '':
            playresponse("error")
    playresponse("cate")
    rawCommand = myCommand()
    for x in GetCategory.supported_cate:
        if x in rawCommand:
            url += GetCategory.supported_cate[x]
    playmp3("response/inform/inform01.mp3")
    all_link = HTMLDom.get_link(url)
    playmp3("response/inform/inform04.mp3")
    for link in all_link:
        title = HTMLDom.get_title(link)
        talkTitle(title)
        x = (count + 1) % 2
        playmp3("{}.mp3".format(x))
        playresponse("confirm")
        command = ""
        while command == "":
            newCommand = myCommand()
            command = Command.comm(newCommand)
            if command == "yes":
                playresponse("download")
                addr = HTMLDom.get_mp3_file(link)
                playresponse("start")
                file = "{}final.mp3".format(addr)
                ended = False
                import pygame
                pygame.init()
                SONG_END = pygame.USEREVENT + 1
                mixer.music.load(file)
                mixer.music.play()
                while True:
                    for event in pygame.event.get():
                        if event.type == SONG_END:
                            print("END!")
                            ended = True
                    if ended:
                        break
                    cmd = Command.comm(listenForCommand())
                    if cmd == "":
                        continue
                    if mixer.music.get_busy():
                        if cmd == 'stop':
                            playresponse("stop")
                            mixer.music.pause()
                        elif cmd == 'escape':
                            mixer.music.stop()
                            break
                    else:

                        if cmd == "resume":
                            playresponse("resume")
                            mixer.music.unpause()
                        elif cmd == 'escape':
                            mixer.music.stop()
                            break
                playresponse("end")
                rawCommand = myCommand()
                if Command.comm(rawCommand) == "yes":
                    import shutil
                    shutil.move(addr, "favourite/{}".format(title))
                    playmp3("response/inform/inform02.mp3")
                playresponse("next")
            elif command == "no":
                playresponse("next")
                continue
            elif command == "escape":
                playmp3("response/inform/inform03.mp3")
                break


def playMusic():
    playresponse("music")
    rawCommand = myCommand()
    import urllib.request
    import urllib.parse
    import re

    query_string = urllib.parse.urlencode({"search_query": rawCommand})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    import webbrowser
    webbrowser.open("http://www.youtube.com/watch?v=" + search_results[0])


playresponse("hello")
while True:
    command = myCommand()
    if "đọc báo" in command:
        readNews()
    elif "nghe nhạc" in command:
        playMusic()
    elif Command.comm(command) == "escape":
        playresponse("escape")
        sys.exit()