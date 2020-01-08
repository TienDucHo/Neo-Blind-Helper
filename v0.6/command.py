supported_command = {
    'pause': ['tạm'],
    'resume': ["trở", "chở lại", "trở lại", "trả"],
    'stop': ['dừng', 'đừng', 'ngừng', 'vừng', 'gừng'],
    'yes': ['ok', 'xác nhận', 'sex nhật', 'phát', 'ừ', 'đồng ý', 'có', 'làm ơn'],
    'no': ['không', 'thôi', 'bỏ', '0'],
    'next': ['tiếp', 'theo', 'qua'],
    'news': ['đọc', 'báo'],
    'music': ['nhạc', 'nhạt'],
    'exit': ['thoát', 'tắt', 'ngắt'],
    'help': ['hỗ trợ', 'giúp']
}

supported_cate = {
    "thời sự": "thoi-su",
    "góc nhìn": "goc-nhin",
    "thế giới": "the-gioi",
    "kinh doanh": "kinh-doanh",
    "giải trí": "giai-tri",
    "thể thao": "the-thao",
    "pháp luật": "phap-luat",
    "giáo dục": "giao-duc",
    "sức khỏe": "suc-khoe",
    "đời sống": "doi-song",
    "du lịch": "du-lich",
    "khoa học": "khoa-hoc",
    "số hóa": "so-hoa",
    "xe": "oto-xe-may",
    "ý kiến": "y-kien",
    "tâm sự": "tam-su",
    "cười": "cuoi",
    "không": "",
    "": ""
}


supported_page = {
    'vnexpress': "https://vnexpress.net/"
}


def getCate(cmd):
    for c in supported_cate:
        if c in cmd:
            return supported_cate[c]

def getCommand(cmd):
    for x in supported_command:
        for y in supported_command[x]:
            if y in cmd:
                return x
