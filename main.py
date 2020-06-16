import command
import recognizer
import extractor
import downloader
import player
import time
import urllib.request
import urllib.error
import wikipedia
import json
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config

main_url = {"vi-VN": "https://vnexpress.net/",
            "en-US": "https://apnews.com/"}
temp_phrases = ['độ C', 'degree Celsius']
lang = ['vi-VN', 'en-US']
lang_code = ['vi', 'en']
lang_id = 0
global_menu = []
global_index = 0
debug_status = 1
weather_key = '3d788c26cd8670e50ea9d876f13da57f'
location_key = '5be117f1bfeb1c8a3f3d796990d5e1c9'


def initiate():
    try:
        urllib.request.urlopen(main_url[lang[lang_id]])
        status = "Connected"
    except urllib.error.HTTPError:
        status = "Not connected"
    except urllib.error.URLError:
        status = "Wrong URL"
    return status


def news(raw):
    print("News Mode activate")
    global global_index
    global global_menu
    global debug_status
    query = "".join(x + ' ' for x in raw.split(" ") if x != 'đọc'
                    and x != 'tin' and x != 'read').strip()
    if query == 'tiếp theo' or query == 'next':
        if global_menu:
            global_index += 1
        else:
            print("Lỗi chưa nạp tin")
            return
    else:
        url = main_url[lang[lang_id]]
        if lang_id == 0:
            url += command.finding_category(query, lang_id)
        global_index = 0
        soup = extractor.make_soup(url)
        query = command.finding_category(query, lang_id)
        global_menu = extractor.get_menu(soup, lang_id, query)
    title_address = downloader.download_menu(global_menu, lang[lang_id])
    news_url = global_menu[global_index][0]
    content = extractor.get_content(news_url)
    num_of_word = 0
    for para in content:
        num_of_word += len(para.split(" "))
    time_now = time.time()
    newest = downloader.download_paragraph(global_menu[global_index][1],
                                           content, lang[lang_id])
    if debug_status:
        with open("log.txt", "a") as log:
            time_elapse = time.time() - time_now
            log.write(f'{time_elapse}s for {num_of_word} words\n')
    media_list = [title_address[global_index]]
    for each in newest[1]:
        media_list.append(each)
    player.play_list(media_list)


def music(raw):
    query = "".join(x+' ' for x in raw.split(" ")
                    if x != 'phát' and x != "hát" and x != 'play')
    print("Music Mode activate")
    print(query)
    video = extractor.youtube_search(query)
    player.play_url('https://www.youtube.com/watch?v=' + video[0])


def player_exit(raw):
    print("Exit Player")
    player.stop()
    time.sleep(2)


def shutdown(raw):
    print(raw)
    exit()


def search(raw):
    query = "".join(x + ' ' for index, x in enumerate(raw.split(" ")) if index > 0)
    wikipedia.set_lang(lang_code[lang_id])
    res = wikipedia.summary(query, sentences=1)
    ans = [downloader.text_to_speech("ans.mp3", res, lang[lang_id],True)]
    player.play_list(ans)


def weather(raw):
    config_dict = get_default_config()
    config_dict['language'] = lang_code[lang_id]
    owm = OWM(weather_key, config_dict)
    loc_url = "http://ipinfo.io/json"
    response = urllib.request.urlopen(loc_url)
    data = json.load(response)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(data['city'])
    weather_now = observation.weather
    temp_dict_celsius = weather_now.temperature('celsius')
    temp = "{} {}".format(temp_dict_celsius['temp_max'], temp_phrases[lang_id])
    para = data['city'] + ' ' + weather_now.detailed_status + ' ' + temp
    add = downloader.text_to_speech("weather.mp3", para, lang[lang_id], True)
    media_list = [add]
    player.play_list(media_list)


def language(raw):
    print(raw)
    global lang_id
    lang_id = (lang_id + 1) % 2
    print(lang[lang_id])


def pause_resume(raw):
    player.pause_resume()


def match_command(raw, cmd):
    print("Command is " + cmd)
    switcher = {
        "news": news,
        "music": music,
        "exit": player_exit,
        "shutdown": shutdown,
        "search": search,
        "weather": weather,
        "language": language,
        "pause": pause_resume,
        "resume": pause_resume
    }
    func = switcher.get(cmd, print)
    if func != print:
        player.playmp3("response/ok.wav")
    else:
        player.playmp3("response/error.wav")
    return func(raw)


if __name__ == "__main__":
    while initiate() != "Connected":
        print("No connection")
        time.sleep(3)
        continue
    print("Neo Online!")
    while True:
        time.sleep(0.1)
        text_command = recognizer.recognize(lang[lang_id]).lower()
        real_command = command.finding_command(text_command)
        if real_command == 'neo':
            player.playmp3("response/ok.wav")
            text_command = recognizer.recognize(lang[lang_id]).lower()
            match_command(text_command, command.finding_command(text_command))
