import speech_recognition as sr
import time

r = sr.Recognizer()
r.energy_threshold = 3000
r.pause_threshold = 1
microphone = sr.Microphone()
json_address = "D:/Code/Neo Blind Helper/Key/credential_json.json"
playing_mode = 0


def read_credential(address):
    result = ""
    with open(address, 'r') as file:
        result += file.read()
    return result


GOOGLE_CLOUD_SPEECH_CREDENTIALS = read_credential(json_address)


def recognize(lang):
    text_cmd = ""
    with microphone as source:
        r.adjust_for_ambient_noise(source)
        r.dynamic_energy_threshold = True
        audio = r.listen(source)
    try:
        text_cmd = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language=lang)
        print("Your command is " + text_cmd)
    except sr.UnknownValueError:
        print("Google Cloud Speech không hiểu được âm thanh")
    except sr.RequestError as e:
        print("Không yêu cầu được kết quả; {0}".format(e))
    time.sleep(0.5)
    return text_cmd
