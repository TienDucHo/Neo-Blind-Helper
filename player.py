import vlc
import pafy
import time

print("Player Initiate")
mlp = vlc.MediaListPlayer()
mp = vlc.MediaPlayer()
lss = []


def playmp3(mp3):
    mp3player = vlc.MediaPlayer(mp3)
    mp3player.play()


def play_list(m_list):
    media_list = vlc.MediaList(m_list)
    mlp.set_media_list(media_list)
    mlp.set_media_player(mp)
    mlp.play()


def play_url(v_url):
    video = pafy.new(v_url)
    best = video.getbest()
    p_url = best.url
    instance = vlc.Instance()
    media = instance.media_new(p_url)
    media.get_mrl()
    lst = [media]
    media_list = vlc.MediaList(lst)
    mlp.set_media_list(media_list)
    mlp.play()


def get_status():
    return mlp.is_playing()


def pause_resume():
    mlp.pause()


def stop():
    mlp.stop()


if __name__ == "__main__":
    this_list = ["D:/Music/GLASSY SKY - dona burke [Lossless_FLAC].flac", "D:/Music/The Realm of Athena.mp3"]
    Instance = vlc.Instance()
    mplayer = Instance.media_player_new()

