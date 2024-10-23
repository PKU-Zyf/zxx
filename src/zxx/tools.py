"""
zxx.tools
小工具
    供其他模块使用的一些工具性函数，不建议在剪辑集锦时直接调用。
"""


from moviepy.editor import *
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from os import path

from .options import GetPath, GetMatchInfo, GetScoreBoardStyle


def str2sec(string: str) -> float:
    """
    字符串转秒数。

    例如：
        str2sec("1:35:36.3")
            返回值：5736.3
    """
    time = string.strip().split(":")
    if len(time) == 3:
        h, m, s = time
    elif len(time) == 2:
        h = 0
        m, s = time
    elif len(time) == 1:
        h, m = 0, 0
        s = time[0]
    else:
        return None
    seconds = 3600 * float(h) + 60 * float(m) + float(s)

    return seconds


def sec2str(seconds: float) -> str:
    """
    秒数转字符串，秒数保留最多三位小数，使用去尾法而非四舍五入。

    例如：
        sec2str(367.57898)
            返回值："06:07.578"
        sec2str(367)
            返回值："06:07"
    """
    m, s = divmod(seconds, 60)

    # 秒数前面补0
    parts = str(s).split(".")
    if len(parts[0]) == 1:
        parts[0] = "0" + parts[0]
    
    # 处理含小数的秒数
    if "." in str(s):
        if len(parts[1]) > 3:
            parts[1] = parts[1][:3]
        s = parts[0] + "." + parts[1]
    else:
        s = parts[0]
    if m == 0:
        return s
    
    h, m = divmod(m, 60)
    if h == 0:
        string = "%02d:%s" % (m, s)
    else:
        string = "%02d:%s" % (h, m, s)
    
    return string


def add_txt_to_img_center(filename: str, text: str, fontpath: str, color: str | tuple):
    """
    在图片正中央添加文字。

    参数说明：
        filename：要加字的图片文件名，工作路径（即 zxx.options.GetPath() 返回值）的相对路径。
        text：要加的文字。
        fontpath：字体文件的路径，注意是绝对路径。
        color：字体颜色，参数值会直接传送给 PIL.ImageDraw.text() 方法的 fill 参数，
            使用色彩名、十六进制、RGB、RGBA 等均可，可采用以下写法中的任意一种：
                color="pink"
                color="#800080"
                color=(255, 10, 10)
                color=(255, 10, 10, 100)
    """

    # 导入图片（解决中文路径乱码问题）
    img_path = path.join(GetPath(), filename)
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    # 读取图片，并手动将 BGR(A) 调整为 RGB(A)
    if filename[-3:] == "png":
        b_channel, g_channel, r_channel, a_channel = cv2.split(img)
        img_RGBA = cv2.merge((r_channel, g_channel, b_channel, a_channel))
        img_pil = Image.fromarray(img_RGBA)
    else:
        b_channel, g_channel, r_channel = cv2.split(img)
        img_RGB = cv2.merge((r_channel, g_channel, b_channel))
        img_pil = Image.fromarray(img_RGB)
    
    # 确定合适的字号
    width, height = img_pil.size
    fontsize = min(int(0.8 * width / len(text)), int(0.8 * height))
    font = ImageFont.truetype(fontpath, fontsize)

    # 精确处理文字位置（居中）
    x_0, y_0, x_1, y_1 = font.getbbox(text)    # 获取边界框，处理可能的 offset
    position = ((width - x_1 - x_0) / 2, (height - y_1 - y_0) / 2)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=color)
    img = np.array(img_pil)
    
    return img


def add_effects(clip: VideoClip, speed: float = 1, silence: bool = False, lum: float = 0, 
            contrast: float = 0, fadein: float = 0, fadeout: float = 0) -> VideoClip:
    """
    为视频片段添加视频特效。

    参数说明：
        clip：要处理的视频片段。类型是 moviepy.video 的 VideoClip 类。
        speed：调整视频的速度倍数，不建议放慢太多，可能导致时间轴错误。
        silence：是否消音。
        lum：亮度要增加或减少的值，大小没有限制，不过一般在 -127 至 127 之间，可自行调试。
        contrast：对比度要调整的值，大小没有限制，不过一般在 -1 至 1之间，可自行调试。
        fadein：淡入效果持续的秒数。
        fadeout：淡出效果持续的秒数。
    """

    # 亮度和对比度
    if lum != 0 or contrast != 0:
        clip = vfx.lum_contrast(clip, lum=lum, contrast=contrast)
    # 变速
    if speed != 1:
        clip_dur = clip.duration
        clip = clip.fl_time(lambda t:speed*t)
        clip = clip.set_duration(clip_dur / speed)
    # 淡入和淡出（变速之后）
    if fadein != 0:
        clip = clip.fx(vfx.fadein, fadein)
    if fadeout != 0:
        clip = clip.fx(vfx.fadeout, fadeout)
    # 消音
    if silence:
        clip = clip.without_audio()

    return clip


def add_caption(clip: VideoClip, text: str) -> VideoClip:
        """
        给视频片段加字幕。
        字幕的字体、字号、颜色、位置等参数，通过 zxx.options.SetCaptionStyle() 统一设置。

        参数说明：
            clip：要加字幕的视频片段。类型是 moviepy.video 的 VideoClip 类。
            text：字幕文案。可以为空字符串。
        """
        from .options import GetCaptionStyle

        # 如果 text 为空，会报错，因此需要打一个空格
        if text == "":
            text = " "
        
        # 按照宽度为 1920 像素的视频的字号，调整字号大小
        video_width = clip.size[0]
        fontsize = GetCaptionStyle("fontsize") / 1920 * video_width
        text_clip = TextClip(
            text,
            font     = GetCaptionStyle("font"),
            fontsize = fontsize,
            color    = GetCaptionStyle("color"),
        ).set_position(GetCaptionStyle("position"), relative=GetCaptionStyle("relative"))
        clip_dur = clip.duration
        clip = CompositeVideoClip([clip, text_clip]).set_duration(clip_dur)
        
        return clip


def add_scoreboard(clip: VideoClip, home: int = 0, away: int = 0) -> VideoClip:
    """
    加比分牌。显示的队名通过 zxx.options.SetMatchInfo() 设置。

    参数说明：
        clip：要加比分牌的视频片段。类型是 moviepy.video 的 VideoClip 类。
        home：主队当前得分。
        away：客队当前得分。
    """

    # 生成比分牌文字内容
    home_name = GetMatchInfo("home")
    away_name = GetMatchInfo("away")
    text = f"{home_name}　{home}-{away}　{away_name}"
    fontpath = path.join(GetPath(), GetScoreBoardStyle("font_file"))
    # 合成比分牌图片
    img = add_txt_to_img_center(
        filename = GetScoreBoardStyle("image"),
        text = text,
        fontpath = fontpath,
        color = GetScoreBoardStyle("color") 
    )
    # 合成图片和视频，比分牌图片的宽度是视频的 1/4
    clip_width = clip.size[0]
    score_width = 0.25 * clip_width
    score_clip = ImageClip(img).fx(vfx.resize, width=score_width)
    # 调整比分牌显示时长
    clip_dur = clip.duration
    clip = CompositeVideoClip([clip, score_clip]).set_duration(clip_dur)

    return clip
