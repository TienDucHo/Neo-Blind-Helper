import os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import sys
import webbrowser
import HTMLDom
import GetCategory
from pygame import mixer

mixer.init()
count = 0
url = ""

#voice
def talkToMe(audio):
    print(audio)
    global count
    nothing = 0
    tts = gTTS(text=audio, lang='vi')
    #text_to_speech.save("{}.mp3".format(count))
    tts.save("{}.mp3".format(count))
    mixer.music.load("{}.mp3".format(count))
    mixer.music.play()
    while mixer.music.get_busy() == True:
        nothing += 0 #do nothing while waiting the mixer to end
    count = (count + 1) % 2
    #playsound("{}.mp3".format(count))
    #os.remove("{}.mp3".format(count))

#listen for commands
def myCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Vui lòng nhập lệnh')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='vi-VI')
        print('Lệnh là ' + command)

    #loop back to continue listening for commands

    except sr.UnknownValueError:
        print('Vui lòng nhập lại')
        command = myCommand();
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
        id = 0
        while id < len(links):
            
            talkToMe(HTMLDom.get_title(links[id]))
            talkToMe("Xác nhận đọc?")
            command = myCommand()
            ex = False
            if "có" or "xác nhận" in command.casefold():
                print(links[id])
                HTMLDom.get_mp3_file(links[id])
                mixer.music.load("audio/full.mp3")
                mixer.music.play()
                while True:
                    command = myCommand()
                    if "dừng đọc" in command.casefold():
                        mixer.music.pause()
                        talkToMe("Dừng đọc. Ngài muốn thoát hẳn?")
                        command = myCommand()
                        if "thoát" or "ừ" or "vâng" or "đúng" in command.casefold():
                            mixer.music.stop()
                            ex = True
                            break
                        else:
                            mixer.music.unpause()
            elif "không" or "tin tiếp theo" in command.casefold():
                id += 1
            elif "dừng đọc" in command.casefold():
                break
            elif ex == True:
                break

def playMusic():
    webbrowser.open("https://www.youtube.com/watch?v=QW8nrxUUxdY")

talkToMe("Chào mừng. Tôi có thể giúp gì cho ngài?")

while True:
    command = myCommand()
    if "đọc báo" in command.casefold():
        readNews()
    elif "nghe nhạc" in command.casefold():
        playMusic()
    elif "tắt máy" or "đi ngủ" or "dừng hoạt động" or "ngưng hoạt động" in command.casefold():
        sys.exit()
        
