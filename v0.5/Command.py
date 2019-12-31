def comm(command):
    if "ừ" in command.casefold():
        return "yes"
    elif "ok" in command.casefold():
        return "yes"
    elif "đồng ý" in command.casefold():
        return "yes"
    elif "chấp nhận" in command.casefold():
        return "yes"
    elif "có" in command.casefold():
        return "yes"
    elif "chắc chắn" in command.casefold():
        return "yes"
    elif "xác nhận" in command.casefold():
        return "yes"
    elif "đọc đi" in command.casefold():
        return "yes"
    elif "danh mục nào" in command.casefold():
        return "category"
    elif "không" in command.casefold():
        return "no"
    elif "bỏ" in command.casefold():
        return "no"
    elif "tin tiếp theo" in command.casefold():
        return "no"
    elif "nghe nhạc" in command.casefold():
        return "music"
    elif "đọc báo" in command.casefold():
        return "news"
    elif "bỏ" in command.casefold():
        return "stop"
    elif "ngừng" in command.casefold():
        return "stop"
    elif "dừng" in command.casefold():
        return "stop"
    elif "tạm ngừng" in command.casefold():
        return "stop"
    elif "đợi" in command.casefold():
        return "stop"
    elif "đừng" in command.casefold():
        return "stop"
    elif "tiếp" in command.casefold():
        return "no"
    elif "lưu" in command.casefold():
        return "favour"
    elif "cho nó vào" in command.casefold():
        return "favour"
    elif "ừm" in command.casefold():
        return "yes"
    elif "tắt máy" in command:
        return "escape"
    elif "dừng hoạt động" in command:
        return "escape"
    elif "đi ngủ" in command:
        return "escape"
    elif "đọc tiếp" in command:
        return "resume"
    elif "trở lại" in command:
        return "resume"
    elif "không đọc" in command:
        return "escape"
    elif "thoát" in command:
        return "escape"
    elif "nghỉ" in command:
        return "escape"
    else:
        return ""

