from bs4 import BeautifulSoup
import os, shutil
import time, requests
import urllib.request

tag = {
    'vnex': ['share_email_right', 'bottom_footer_1', 'bottom_footer_2', 'coppy_right_left', 'row_menu_tablet']
}

api_key = "0bf528396c8146268c5eb01bf1f51bd8"
voice = "female"
speed = "0"
prosody = "1"
url = \
    "http://api.openfpt.vn/text2speech/v4?api_key={}&voice={}&speed={}&prosody={}".\
        format(api_key, voice, speed,
                                                                                            prosody)

def gettext(link):
    re = requests.get(link)
    html = re.text
    soup = BeautifulSoup(html, 'html.parser')
    text = ""
    allp = soup.find_all("p")
    for content in allp:
        if content.find("span"):
            for span in content("span"):
                if span.has_attr("class"):
                    span.decompose()
        if content.find("strong"):
            continue
        if content.find("a"):
            kta = False
            for elema in content("a"):
                if not elema.has_attr('rel'):
                    kta = True
                    break
            if kta:
                continue
        if content.parent.has_attr("class"):
            kt = True
            for cl in tag['vnex']:
                if cl in content.parent["class"]:
                    kt = False
                    break
            if not kt:
                continue

        text += content.get_text()
    word_count = len(text.split(" "))
    return word_count, text


def getmp3(link):
    t = time.time()
    letter_count = 0
    word_count, para = gettext(link)
    para = para.split("\n")
    para = [x for x in para if x != ""]
    title, sp_title = gettitle(link)
    sp_title = sp_title.replace("/", " tháng ")
    sp_title ="".join(ch for ch in sp_title if ch.isalnum() or ch == " ")
    file_addr = os.path.join("news", "{}.mp3".format(sp_title))
    if os.path.exists(file_addr):
        return
    for content in para:
        letter_count += len(content)
        r = requests.post(url, data=content.encode('utf-8'),
                          headers={'voice': voice, 'speed': speed, 'prosody': prosody})
        file = r.json()['async']
        download_tries = 100
        while download_tries > 0:
            try:
                with urllib.request.urlopen(file) as response, open(
                        file_addr, 'ab') as out_file:
                    shutil.copyfileobj(response, out_file)
            except:
                download_tries = download_tries - 1
                continue
            else:
                break
        print(">", end="")
    t = time.time() - t
    with open("log.txt", "a") as logger:
        logger.write("{} {} {}\n".format(word_count, t, word_count/t))
    return file_addr


def gettitle(link):
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find("h1")
    sp_title = soup.find("h1", class_="title_news_detail mb10")
    return title.get_text(), sp_title.get_text()


def gethyper(link):
    list_of_link = []
    r = requests.get(link)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find_all("h4", class_="title_news")
    big_title = soup.find_all("h1", class_="title_news")
    for a in big_title:
        list_of_link.append(a.find("a")['href'])
    for a in title:
        t = a.find("a")
        list_of_link.append(t['href'])
    return list_of_link
