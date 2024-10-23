"""
zxx.options
全局设置
    存储全局设置的一些参数，以及修改这些参数的接口。
"""


# 以下全局设置相关的参数，及其默认值
# 想要查看或修改这些参数，请勿直接调用这些变量，而是应当使用本模块提供的相应函数。

PATH = "D:\\"

MATCH_INFO = {
    "home": "政信信",
    "away": "",
}

CAPTION_STYLE = {
    "font": "楷体",
    "fontsize": 100,    # 一行大约19个汉字
    "color": "white",
    "position": "bottom",
    "relative": False,
}

SCOREBOARD_STYLE = {
    "image": "scoreboard.png",
    "font_file": "华文新魏.ttf",
    "color": "black",
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
        font="楷体",
        fontsize=100,
        color="white",
        position="bottom",
        relative=False,

    参数说明：
        font、fontsize 和 color 参数都是传入 moviepy.video.VideoClip 的 TextClip 类的初始化参数 font。
        font：直接键入字体名即可，但必须是在 zxx.options.AllFonts() 返回的字体列表中的字体名。
        fontsize：字号，可调试后调整数字大小。
        color：字体颜色。须符合 ImageMagick 的颜色写法，使用色彩名、十六进制、RGB、RGBA 等均可，
            可采用以下写法中的任意一种：
                color="lime"
                color="#00ff00"
                color="rgb(0, 255, 0)"
                color="rgba(0, 255, 0, 1.0)"
            详见：https://imagemagick.org/script/color.php
        position 和 relative：传入 TextClip.set_position() 函数，可以使用多种写法。
            set_position() 函数示例翻译如下：
                clip.set_position((45,150))    # 像素坐标 x=45, y=150
                clip.set_position(("center","top"))    # 水平居中，竖直对齐
                clip.set_position((0.4,0.7), relative=True)    # 相对位置，水平 40%，竖直 70%
                clip.set_position(lambda t: ('center', 50+t) )    # 水平居中，竖直向上移动
            对应地，使用本函数时，直接写成：
                position=(45,150)
                position="bottom"
                position=("center","top")
                position=(0.4,0.7), relative=True
                position=lambda t: ('center', 50+t)
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

    参数说明：
        image：比分牌图片的文件名，工作路径（即 zxx.options.GetPath() 返回值）的相对路径。最好是细长的横版图片。
        font_file：字体文件名，需要把字体文件复制到工作路径。
        color：字体颜色。须符合 Pillow 库的颜色写法，使用色彩名、十六进制、RGB、RGBA 等均可，
            可采用以下写法中的任意一种：
                color="pink"
                color="#800080"
                color=(255, 10, 10)
                color=(255, 10, 10, 100)
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


def AllFonts(print_list: bool = True) -> list:
    """
    返回所有可用的字体列表。

    参数说明：
        print_list：是否打印字体列表，默认打印。
    """
    from moviepy.editor import TextClip

    font_list = TextClip.list("font")
    if print_list:
        print(font_list)
    
    return font_list
