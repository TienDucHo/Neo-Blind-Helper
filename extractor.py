from bs4 import BeautifulSoup
import urllib.request
import json
from newsplease import NewsPlease
import googleapiclient.discovery
import googleapiclient.errors

left_out_tag = ['share_email_right', 'bottom_footer_1', 'bottom_footer_2', 'coppy_right_left', 'row_menu_tablet',
                'article-oldnew-brief', 'article-oldnew-brief-time',
                'footer-content-left', 'footer-content-right']

nyt_api = 'qNIkufLSycIQRfZm3ARgFkqi6wdSvfKJ'


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def youtube_search(query):
    api_service_name = "youtube"
    api_version = "v3"
    key = "AIzaSyD0CozLa4ftbTfn8ccBGegXm-6n6MoORQU"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)

    request = youtube.search().list(
        part="snippet",
        maxResults=3,
        q=query
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    video_title = response['items'][0]['snippet']['title'].replace('&amp;', '&')
    print(video_title)
    return [video_id, video_title]


def make_soup(link):
    req = urllib.request.urlopen(link)
    soup = BeautifulSoup(req, 'html.parser')
    return soup


def determine(elem):
    if elem.parent.has_attr('class'):
        for tag in left_out_tag:
            if tag in elem.parent['class']:
                return True
    if elem.find('a'):
        for a in elem('a'):
            if not a.has_attr("rel"):
                return True


def get_content(news_url):
    article = NewsPlease.from_url(news_url)
    content = (article.description + '\n' + article.maintext).split('\n')
    return content


def get_title(soup):
    return soup.find('h1').get_text()


def get_menu(soup, lang, section='home'):
    if lang == 0:
        menu = [(elem['href'], elem['title']) for elem in soup.find_all('a')
                if elem.has_attr("data-thumb") and elem.has_attr("title") and not elem.has_attr('rel')]
        menu = list(dict.fromkeys(menu))
        return menu
    else:
        api_url = f'https://api.nytimes.com/svc/topstories/v2/{section}.json'
        api_url += f'?api-key={nyt_api}'
        print(api_url)
        req = urllib.request.urlopen(api_url)
        req = json.load(req)
        ret = []
        if req['status'] == 'OK':
            for each in req['results']:
                ret.append([each['url'], each['title']])
            return ret


def get_youtube_url(soup):
    all_vid = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
    identity = []
    for each_vid in all_vid:
        identity.append(each_vid['href'])
    return identity


if __name__ == "__main__":
    url = 'https://apnews.com/'
    print(get_menu(make_soup(url), 1)[0])
