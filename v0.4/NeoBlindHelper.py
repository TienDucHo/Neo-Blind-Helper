import os
import sys

import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

import Command
import GetCategory
import HTMLDom

mixer.init(buffer=1024)
count = 0
url = ""


# voice
def talkToMe(audio):
    print(audio)
    global count
    nothing = 0
    tts = gTTS(text=audio, lang='vi')
    tts.save("{}.mp3".format(count))
    mixer.music.load("{}.mp3".format(count))
    mixer.music.play()
    while mixer.music.get_busy() == True:
        nothing += 0  # do nothing while waiting the mixer to end
    count = (count + 1) % 2


# listen for commands
def myCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Vui lòng nhập lệnh')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='vi-VI')
        print('Lệnh là ' + command)
    # loop back to continue listening for commands
    except sr.UnknownValueError:
        print('Vui lòng nhập lại')
        command = myCommand()
    return command


def readNews():
    talkToMe("Xác nhận. Ngài muốn đọc báo nào?")
    command = myCommand()
    if "vnexpress" in command.casefold():
        url = "https://vnexpress.net"
        talkToMe("Xác nhận. Ngài cần danh mục cụ thể không?")
        url = url + "/" + GetCategory.get_category(myCommand())
        links = HTMLDom.get_link(url)
        talkToMe("Xác nhận. Phát tin đầu tiên")
        id: int = 0
        while id < len(links):
            talkToMe(HTMLDom.get_title(links[id]))
            talkToMe("Xác nhận đọc?")
            ncommand = Command.comm(myCommand())
            ex = False
            if ncommand == "yes":
                talkToMe("Đang tải tin")
                address = HTMLDom.get_mp3_file(links[id])
                talkToMe("Bắt đầu đọc")
                for filename in os.listdir(address):
                    if filename.endswith(".mp3"):
                        file = "{}{}".format(address, filename)
                        print(file)
                        mixer.music.load(file)
                        mixer.music.play()
                        nothing = 0
                        while mixer.music.get_busy():
                            nothing += 0
                # do nothing while waiting the mixer to end
                id += 1
                talkToMe("Kết thúc tin. Tin tiếp theo")
            else:
                if ncommand == "no":
                    print("Tin tiếp theo...")
                    id += 1
                    continue
                else:
                    if ncommand == "stop":
                        talkToMe("Thoát khỏi báo!")
                        return
                    else:
                        if ex == True:
                            break


def playMusic():
    print("Nghe nhạc")
    # webbrowser.open("https://www.youtube.com/watch?v=QW8nrxUUxdY")


talkToMe("Chào mừng. Tôi có thể giúp gì cho ngài?")

while True:
    command = myCommand()
    if "đọc báo" in command.casefold():
        readNews()
    elif "nghe nhạc" in command.casefold():
        playMusic()
    elif "tắt máy" in command.casefold() or "đi ngủ" in command.casefold() or "dừng hoạt động" in command.casefold() or "ngưng hoạt động" in command.casefold():
        sys.exit()
