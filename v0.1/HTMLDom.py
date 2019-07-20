from htmldom import htmldom #for html parser
import requests #for html post
import json #for extracting json
import os #create folder
import wget #download file without open
import subprocess #merging mp3 file
from bs4 import BeautifulSoup #another html parser cause sometimes htmldom is suck

def get_mp3_file(link): #like the name says, it make mp3 out of a link
     
    api_key = "0bf528396c8146268c5eb01bf1f51bd8"
    voice = "female"
    speed = "0"
    prosody = "1"

    local_path = "audio"
    

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    if os.path.exists("{}/full.mp3".format(local_path)):
        os.remove("{}/full.mp3".format(local_path))
    
    url = "http://api.openfpt.vn/text2speech/v4?api_key={}&voice={}&speed={}&prosody={}".format(api_key, voice, speed, prosody)

    news = link

    #this section is for html parse -> get the content of the paper
    dom = htmldom.HtmlDom(news)
    dom = dom.createDom()
    elem = dom.find("p.Normal")

    #this section is for calling api and download the mp3 files
    id = 1
    for content in elem:
        r = requests.post(url, data = content.text().encode('utf-8'), headers={'voice':voice, 'speed':speed, 'prosody':prosody})
        r = r.json()
        file = r['async']
        wget.download(file, "{}/{:03}.mp3".format(local_path,id))
        id += 1
        #print(r['async']) #print(content.text())

    # this section is for merging the mp3 file
    f = open("{}/create_list.bat".format(local_path), "w")
    f.write("(for %%i in (*.mp3) do @echo file '%%i') > list.txt")
    f.close()

    s = "{}/create_list.bat".format(local_path)
    os.chdir(local_path)
    subprocess.Popen("create_list.bat")
    os.chdir('..')

    p = subprocess.run('ffmpeg -f concat -safe 0 -i {}/list.txt -c copy {}/full.mp3'.format(local_path, local_path))

    #this section is for cleaning up the file
    new_id = 1
    while new_id < id:
        os.remove("{}/{:03}.mp3".format(local_path,new_id))
        new_id += 1
    os.remove("audio/create_list.bat")
    os.remove("audio/list.txt")

def get_link(link): #extract all the link it could from a link
    list_of_link = []
    dom = htmldom.HtmlDom(link)
    dom = dom.createDom()
    big_title = dom.find("h1.title_news")
    r  = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find_all("h4", class_= "title_news")
    for a in title:
        t = a.find("a")
        list_of_link.append(t['href'])
        #str.replace(t,"&nbsp;","")
        #print(t['href'])
    return list_of_link

def get_title(link):
    r  = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find("h1")
    return title.get_text()

