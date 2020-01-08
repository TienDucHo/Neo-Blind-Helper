import os, shutil
import speech_recognition as sr
import random
from gtts import gTTS
from pygame import mixer
import time

import command
import extractor

mixer.init(buffer=8192)
count = 0
url = ""
resp = "response"
debug = False


def idle():
    while mixer.music.get_busy():
        continue


def playmp3(address, idle_stat):
    mixer.music.load(address)
    mixer.music.play()
    if idle_stat:
        idle()


def voice(text):
    global count
    tts = gTTS(text=text, lang='vi')
    tts.save("util/{}.mp3".format(count))
    playmp3("util/{}.mp3".format(count), True)
    count = (count + 1) % 2


def responsing(type):
    addr = os.path.join(resp, type)
    id = random.randint(1, len(os.listdir(addr)))
    mixer.music.load(os.path.join(addr, "{}{:02}.mp3".format(type, id)))
    mixer.music.play()
    idle()


def listenForCommand():
    print("Listening...")
    res = ""
    recog = sr.Recognizer()
    with sr.Microphone() as source:
        recog.pause_threshold = 0.5
        recog.adjust_for_ambient_noise(source, duration=0.5)
        audio = recog.record(source, duration=3.2)
    try:
        res = recog.recognize_google(audio, language='vi-VI')
        print("Command is " + res)
    except sr.UnknownValueError:
        print("Failed")
    return res.casefold()


def check(req):
    flag_p = False
    global url
    for x in command.supported_page:
        if x in req:
            flag_p = True
            url = command.supported_page[x]
    return flag_p


def news():
    responsing("news")
    print("Đọc báo mode on")
    global url
    raw = listenForCommand()
    time.sleep(0.2)
    while not check(raw):
        raw = listenForCommand()
    url += command.getCate(raw)
    lnk = extractor.gethyper(url)
    playmp3("response/inform/inform04.mp3", True)
    for link in lnk:
        ti, sp_ti = extractor.gettitle(link)
        voice(sp_ti)
        responsing("confirm")
        while True:
            confirmation = command.getCommand(listenForCommand())
            if confirmation == "yes":
                responsing("download")
                addr = ""
                addr = extractor.getmp3(link)
                while addr == "":
                    continue
                responsing("start")
                playmp3(addr, False)
                return True
            elif confirmation == "next":
                responsing("next")
                break
            elif confirmation == "exit":
                playmp3("response/inform/inform05.mp3", True)
                return True
    return True


def music():
    responsing("music")
    raw = listenForCommand()
    if command.getCommand(raw) == "escape":
        playmp3("response/inform/inform06.mp3", True)
        return True
    playmp3("response/inform/inform07.mp3", True)
    import urllib.request
    import urllib.parse
    import re
    query_string = urllib.parse.urlencode({"search_query": raw})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    import youtube_dl

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': "music/%(title)s.%(ext)s"
    }
    file = ""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info("http://www.youtube.com/watch?v=" + search_results[0])
        text = ydl.prepare_filename(file)
        #ydl.download(["http://www.youtube.com/watch?v=" + search_results[0]])
    text = os.path.splitext(text)[0]
    playmp3(text+".mp3", False)
    return True


responsing("hello")


if not debug:
    while True:
        cmd = command.getCommand(listenForCommand())
        if cmd is "news":
            news()
        elif cmd is "music":
            music()
        elif cmd is "pause":
            if mixer.music.get_busy():
                mixer.music.pause()
        elif cmd is "resume":
            if mixer.music.get_busy():
                mixer.music.unpause()
        elif cmd is "stop":
            mixer.music.stop()
        elif cmd is "exit":
            import sys
            responsing("escape")
            sys.exit()

else:
    voice("Đang tải nhạc, vui lòng đợi")
