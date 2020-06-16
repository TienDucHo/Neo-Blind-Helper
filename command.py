supported_command = {
    'resume': ["trở", "chở lại", "trở lại", "trả", 'unpause', 'resume'],
    'pause': ['tạm', 'dừng', 'đừng', 'ngừng', 'vừng', 'gừng', 'pause'],
    'yes': ['ok', 'xác nhận', 'sex nhật', 'ừ', 'đồng ý', 'có', 'nhật'],
    'no': ['không', 'thôi', 'bỏ', '0'],
    'next': ['tiếp', 'theo', 'qua'],
    'news': ['đọc', 'báo', 'read'],
    'music': ['nhạc', 'nhạt', 'phát', 'hát', 'play'],
    'exit': ['thoát', 'exit'],
    'shutdown': ['tắt', 'shut'],
    'help': ['hỗ trợ', 'giúp', 'hỗ', "trợ", 'help'],
    'neo': ['neo', 'mèo', 'meo', 'nhèo', 'nheo', 'nghèo', 'ngheo', 'miu', 'news', 'mios', 'meomeo', 'meou', 'meow'],
    'language': ['tiếng', 'anh', 'vietnamese'],
    'weather': ['thời tiết', 'thời', 'tiết', 'weather'],
    'search': ['tra', 'cứu', 'tìm', 'search']
}

supported_cate = [{
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
    "mới nhất": ""
}, {
    "": "home",
    "all": "home",
    "newest": "home",
    "newspaper": "home",
    "home": "home"
},
]


def finding_command(text):
    for word in text.split(" "):
        for x in supported_command:
            if word in supported_command[x]:
                return x
    return "None"


def finding_category(text, lang_id):
    for x in supported_cate[lang_id]:
        if x in text:
            return supported_cate[lang_id][x]
    return "" if lang_id == 0 else text

