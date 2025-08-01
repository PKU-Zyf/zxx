"""
zxx.options
全局设置
    存储全局设置的一些参数，以及修改这些参数的接口。
"""


# 以下全局设置相关的参数，及其默认值
# 想要查看或修改这些参数，请勿直接调用这些变量，而是应当使用本模块提供的相应函数。

PATH = "D:\\"

MATCH_INFO = {
    "home": "政信社",
    "away": "友队",
}

CAPTION_STYLE = {
    "font": "C:\\Windows\\Fonts\\simkai.ttf",
    "fontsize": 100,    # 一行大约19个汉字
    "color": "white",
    "position": "bottom",
    "relative": False,
}

SCOREBOARD_STYLE = {
    "image": "scoreboard.png",
    "font_file": "华文新魏.ttf",
    "color": "black",
    "width_factor": 0.25,
}


# 以下是修改设置的函数

def SetPath(path: str) -> None:
    """
    设置工作路径（绝对路径）。
    """
    global PATH
    PATH = path


def SetMatchInfo(**kwargs) -> None:
    """
    设置比赛信息。可以传入任意的参数，无效的参数会被忽略。

    可以识别的参数及其默认值：
        home="政信信",
        away="",

    参数说明：
        指定主队和客队的队名，会显示在比分牌上。
    """
    global MATCH_INFO
    MATCH_INFO.update(kwargs)


def SetCaptionStyle(**kwargs) -> None:
    """
    修改字幕设置。可以传入任意的参数，无效的参数会被忽略。

    可以传入的参数及其默认值：
        font="C:\\Windows\\Fonts\\simkai.ttf",
        fontsize=100,
        color="white",
        position="bottom",
        relative=False,

    参数说明：
        font：需指定字体文件路径，必须是 OpenType 字体格式。
            可采用绝对路径，例如："C:\\Windows\\Fonts\\simkai.ttf"；
            也可采用相对路径，例如 "simkai.ttf"，此时将在工作路径下寻找该字体文件。
        fontsize：字号，可调试后调整数字大小。
        color：字体颜色。须符合 Pillow 库的命名规范，使用色彩名、十六进制、RGB、RGBA 均可，
            可采用以下写法中的任意一种：
                color="lime"
                color="#00ff00"
                color="(0, 255, 0)"
                color="(0, 255, 0, 1.0)"
        position 和 relative：设置字幕位置，可以使用多种写法。
            这两个参数直接传入 moviepy 的 TextClip.with_position() 方法，使用 SetCaptionStyle() 时直接写成：
                position=(45,150)    # 像素坐标 x=45, y=150
                position="bottom"    # 竖直底对齐
                position=("center","top")    # 水平居中，竖直上对齐
                position=(0.4,0.7), relative=True    # 相对位置，水平 40%，竖直 70%
                position=lambda t: ('center', 50+t)    # 水平居中，竖直向上移动
    """
    global CAPTION_STYLE
    CAPTION_STYLE.update(kwargs)


def SetScoreBoardStyle(**kwargs) -> None:
    """
    修改比分牌设置。可以传入任意的参数，无效的参数会被忽略。

    可以传入的参数及其默认值：
        image="scoreboard.png",
        font_file="华文新魏.ttf",
        color="black",
        width_factor=0.25,

    参数说明：
        image：比分牌图片的文件名，工作路径（即 zxx.options.GetPath() 返回值）的相对路径。最好是细长的横版图片。
        font_file：字体文件名，需要把字体文件复制到工作路径。
        color：字体颜色。须符合 Pillow 库的颜色写法，使用色彩名、十六进制、RGB、RGBA 等均可，
            可采用以下写法中的任意一种：
                color="pink"
                color="#800080"
                color=(255, 10, 10)
                color=(255, 10, 10, 100)
        width_factor：比分牌宽度占视频宽度的比例。
    """
    global SCOREBOARD_STYLE
    SCOREBOARD_STYLE.update(kwargs)


# 以下是读取设置的函数

def GetPath() -> str:
    """
    返回当前设置的工作路径。
    """
    return PATH


def GetMatchInfo(para: str = None) -> dict | str:
    """
    返回比赛信息。
    如果具体指定需要某个参数，则返回该参数的值；如果未指定，返回所有比赛信息。
    """
    if para == None:
        return MATCH_INFO
    
    else:
        return MATCH_INFO[para]


def GetCaptionStyle(para: str = None) -> dict | str:
    """
    返回字幕设置。
    如果具体指定需要某个参数，则返回该参数的值；如果未指定，返回所有字幕设置。
    """
    if para == None:
        return CAPTION_STYLE
    
    else:
        return CAPTION_STYLE[para]
 
    
def GetScoreBoardStyle(para: str = None) -> dict | str:
    """
    返回比分牌设置。
    如果具体指定需要某个参数，则返回该参数的值；如果未指定，返回所有比分牌设置。
    """
    if para == None:
        return SCOREBOARD_STYLE
    
    else:
        return SCOREBOARD_STYLE[para]


def AllFonts(print_list: bool = True) -> None:
    """
    （已弃用）返回所有可用的字体列表。
    由于 moviepy 2.x 不再依赖 ImageMagick，改为直接指定字体路径，因此不再需要这一功能。
    """

    print("AllFonts() 方法已被弃用，因为 zxx 1.2.0 及以后版本依赖的 moviepy 2.x 可直接指定字幕字体路径。")
    return None
