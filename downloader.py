import os
import concurrent.futures
import extractor
from google.cloud import texttospeech


def text_to_speech(address, text, lang, overwrite=False):
    if not os.path.exists(address) or overwrite:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(address, "wb") as out:
            out.write(response.audio_content)
            print('Download thành công')
            return address

    return address


def download_paragraph(a_title, paragraph, lang):
    clean_title = "news/"+"".join(char for char in a_title if char.isalnum() or char == " ")
    parts = [f'{clean_title} {index:02d}.mp3' for index, _ in enumerate(paragraph)]
    ret = []
    language = [lang for _ in paragraph]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(text_to_speech, parts, paragraph, language)
        for rete in results:
            ret.append(rete)
    return [clean_title, ret]


def download_menu(menu, lang):
    titles = [x for _, x in menu]
    clean_titles = []
    ret = []
    language = [lang for _, _ in menu]
    for t in titles:
        clean_titles.append("".join(x for x in t if x.isalnum() or x == ' '))
    title_address = [f'title/{clean_title}.mp3' for clean_title in clean_titles]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(text_to_speech, title_address, titles, language)
        for each in results:
            ret.append(each)
    return ret


if __name__ == "__main__":
    url = "https://vnexpress.net/29-nguoi-bi-de-nghi-truy-to-trong-vu-an-o-dong-tam-4114612.html"
    soup = extractor.make_soup(url)
    content = extractor.get_content(soup)
    title = extractor.get_title(soup)
    download_paragraph(title, content)
