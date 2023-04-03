"""
全局设置

"""

# 以下是默认设置

PATH = "D:\\"

MATCH_INFO = {
    "home": "政信信",
    "away": ""
}

CAPTION_STYLE = {
    "font": "华文新魏",
    "fontsize": 100,    # 一行大约19个汉字
    "color": "white",
    "position": "bottom",
}

SCOREBOARD_STYLE = {
    "image": "scoreboard.png",
    "font_file": "华文新魏.ttf",
    "color": "black",
}

# 以下是修改设置的函数

def SetVideoPath(path):
    global PATH
    PATH = path

def SetMatchInfo(**kwargs):
    global MATCH_INFO
    MATCH_INFO.update(kwargs)

def SetCaptionStyle(**kwargs):
    global CAPTION_STYLE
    CAPTION_STYLE.update(kwargs)

def SetScoreBoardStyle(**kwargs):
    global SCOREBOARD_STYLE
    SCOREBOARD_STYLE.update(kwargs)

# 以下是读取设置的函数

def GetPath():
    return PATH

def GetMatchInfo(para:str=None):
    if para == None:
        return MATCH_INFO
    else:
        return MATCH_INFO[para]

def GetCaptionStyle(para:str=None):
    if para == None:
        return CAPTION_STYLE
    else:
        return CAPTION_STYLE[para]
    
def GetScoreBoardStyle(para:str=None):
    if para == None:
        return SCOREBOARD_STYLE
    else:
        return SCOREBOARD_STYLE[para]
