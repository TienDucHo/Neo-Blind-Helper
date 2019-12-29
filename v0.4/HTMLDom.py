import requests #for html post
import os #create folder
from bs4 import BeautifulSoup
import shutil
from unidecode import unidecode

vnEx = ['share_email_right', 'bottom_footer_1', 'bottom_footer_2', 'coppy_right_left', 'row_menu_tablet']

def get_Text(link):
    re = requests.get(link)
    html = re.text
    soup = BeautifulSoup(html, 'html.parser')
    text = ""
    all = soup.find_all("p")
    for content in all:
        if content.find("span"):
            for span in content("span"):
                span.decompose()
        if content.find("strong"):
            content.strong.decompose()
            continue
        if content.find("a"):
            for a in content("a"):
                a.decompose()
            continue
        if content.parent.has_attr("class"):
            kt = True
            for cl in vnEx:
                if cl in content.parent["class"]:
                    kt = False
                    break
            if not kt:
                continue
        text += content.get_text()
    return text


def get_mp3_file(link): #like the name says, it makes mp3 out of a link
     
    api_key = "0bf528396c8146268c5eb01bf1f51bd8"
    voice = "female"
    speed = "0"
    prosody = "1"

    local_path = "news"

    folder_name = ""
    news_title = get_specific_title(link).casefold().replace("\n", "")
    news_title = unidecode(news_title).casefold()

    for c in news_title:
        if c.isalpha() or c == " ":
            folder_name += c

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    if os.path.exists("{}/{}/".format(local_path, folder_name)):
        shutil.rmtree("{}/{}/".format(local_path, folder_name), ignore_errors=True)

    if not os.path.exists("{}/{}/".format(local_path, folder_name)):
        os.makedirs("{}/{}/".format(local_path, folder_name))
    
    url = "http://api.openfpt.vn/text2speech/v4?api_key={}&voice={}&speed={}&prosody={}".format(api_key, voice, speed, prosody)
    paragraph = get_Text(link).split('\n')
    for x in paragraph:
        if x == '':
            paragraph.remove(x)
    #this section is for calling api and download the mp3 files
    id = 1
    nothing = 0
    for content in paragraph:
        r = requests.post(url, data=content.encode('utf-8'), headers={'voice':voice, 'speed':speed, 'prosody':prosody})
        r = r.json()
        file = r['async']
        mp3 = requests.get(file)
        open("{}/{}/{:03}.mp3".format(local_path, folder_name, id), "wb").write(mp3.content)
        id += 1
        print(">", end="")

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
