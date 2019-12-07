import requests #for html post
import json #for extracting json
import os #create folder
import wget #download file without open
from bs4 import BeautifulSoup #another html parser cause sometimes htmldom is suck
import time
import shutil
from unidecode import unidecode

def get_mp3_file(link): #like the name says, it makes mp3 out of a link
     
    api_key = "0bf528396c8146268c5eb01bf1f51bd8"
    voice = "female"
    speed = "0"
    prosody = "1"

    local_path = "news"

    re = requests.get(link)
    data = re.text
    soup = BeautifulSoup(data, 'html.parser')
    
    folder_name = get_specific_title(link).casefold().replace("\n","")

    folder_name = unidecode(folder_name).casefold()
    

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    if os.path.exists("{}/{}/".format(local_path, folder_name)):
        shutil.rmtree("{}/{}/".format(local_path, folder_name))

    if not os.path.exists("{}/{}/".format(local_path, folder_name)):
        os.makedirs("{}/{}/".format(local_path, folder_name))
    
    url = "http://api.openfpt.vn/text2speech/v4?api_key={}&voice={}&speed={}&prosody={}".format(api_key, voice, speed, prosody)

    news = link

    #this section is for html parse -> get the content of the paper
    
    elem = soup.find_all("p", class_="Normal")

    #this section is for calling api and download the mp3 files
    id = 1
    for content in elem:
        r = requests.post(url, data=content.text.encode('utf-8'), headers={'voice':voice, 'speed':speed, 'prosody':prosody})
        time.sleep(4)
        r = r.json()
        file = r['async']
        wget.download(file, "{}/{}/{:03}.mp3".format(local_path, folder_name, id))
        id += 1
        print(">", end="")

    # this section is for merging the mp3 file
    '''f = open("{}/create_list.bat".format(local_path), "w")
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
        os.remove("{}/{:03}.mp3".format(local_path, new_id))
        new_id += 1
    os.remove("audio/create_list.bat")
    os.remove("audio/list.txt")'''
    print("Finish!")
    return "{}/{}/".format(local_path, folder_name)


def get_link(link): #extract all the link it could from a link
    list_of_link = []
    r  = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find_all("h4", class_= "title_news")
    big_title = soup.find("h1.title_news")
    for a in title:
        t = a.find("a")
        list_of_link.append(t['href'])
    return list_of_link

def get_title(link):
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find("h1")
    return title.get_text()

def get_specific_title(link):
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find("h1", class_="title_news_detail mb10")
    return title.get_text()

