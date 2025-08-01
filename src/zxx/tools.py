"""
zxx.tools
小工具
    供其他模块使用的一些工具性函数，不建议在剪辑集锦时直接调用。
"""


from moviepy import VideoClip


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
        sec2str(367.00)
            返回值："06:07"
        sec2str(367.0001)
            返回值："06:07.000"
    """
    m_f, s_f = divmod(seconds, 60)    
    s = str(s_f)

    # 删去小数部分末尾多余的 0
    # 如果小数部分全是 0 则连同小数点一起删除
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    # 秒数前面补 0
    parts = s.split(".")
    if len(parts[0]) == 1:
        parts[0] = "0" + parts[0]
    # 处理含小数的秒数，去尾法保留 3 位
    if "." in s:
        if len(parts[1]) > 3:
            parts[1] = parts[1][:3]
        s = parts[0] + "." + parts[1]
    else:
        s = parts[0]
    if m_f == 0:
        return s
    
    h_f, m_f = divmod(m_f, 60)
    if h_f == 0:
        string = "%02d:%s" % (m_f, s)
    else:
        string = "%02d:%02d:%s" % (h_f, m_f, s)

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
    import cv2
    from PIL import ImageFont, ImageDraw, Image
    import numpy as np
    from os.path import join
    from .options import GetPath

    # 导入图片（解决中文路径乱码问题）
    img_path = join(GetPath(), filename)
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


def add_effects(clip: VideoClip, speed: float = 1, duration: float | None = None, silence: bool = False, lum: float = 0, 
            contrast: float = 0, fadein: float = 0, fadeout: float = 0) -> VideoClip:
    """
    为视频片段添加视频特效。

    参数说明：
        clip：要处理的视频片段。类型是 moviepy 的 VideoClip 类。
        speed：调整视频的速度倍数。不可以和 duration 参数一起指定。默认为 1。不建议放慢太多，可能导致时间轴错误。
        duration：调整视频的速度后，视频片段的持续时间（秒数）。不可以和 speed 参数一起指定。默认为 None。
        silence：是否消音。
        lum：亮度要增加或减少的值，大小没有限制，不过一般在 -127 至 127 之间，可自行调试。
        contrast：对比度要调整的值，大小没有限制，不过一般在 -1 至 1之间，可自行调试。
        fadein：淡入效果持续的秒数。
        fadeout：淡出效果持续的秒数。
    """
    from moviepy.video import fx as vfx
    from moviepy.audio import fx as afx

    # 亮度和对比度
    if lum != 0 or contrast != 0:
        clip = clip.with_effects([vfx.LumContrast(lum=lum, contrast=contrast)])
    # 变速
    if speed != 1 and duration is not None:
        raise Exception("只能同时指定`speed`和`duration`中的一个噢！请重新设置参数。")
    elif speed != 1:
        clip = clip.with_effects([vfx.MultiplySpeed(factor=speed)])
    elif duration is not None:
        clip = clip.with_effects([vfx.MultiplySpeed(final_duration=duration)])
    # 淡入和淡出（变速之后）
    if fadein != 0:
        clip = clip.with_effects([vfx.FadeIn(duration=fadein)])
    if fadeout != 0:
        clip = clip.with_effects([vfx.FadeOut(duration=fadeout)])
    # 消音
    if silence:
        clip = clip.with_effects([afx.MultiplyVolume(factor=0)])

    return clip


def add_caption(clip: VideoClip, text: str) -> VideoClip:
        """
        给视频片段加字幕。
        字幕的字体、字号、颜色、位置等参数，通过 zxx.options.SetCaptionStyle() 统一设置。

        参数说明：
            clip：要加字幕的视频片段。类型是 moviepy.video 的 VideoClip 类。
            text：字幕文案。可以为空字符串。
        """
        from moviepy import TextClip, CompositeVideoClip
        from os.path import join
        from .options import GetCaptionStyle, GetPath

        # 如果 text 为空，会报错，因此需要打一个空格
        if text == "":
            text = " "
        # 按照宽度为 1920 像素的视频的字号，调整字号大小
        video_width = clip.size[0]
        fontsize = GetCaptionStyle("fontsize") / 1920 * video_width
        font_path = GetCaptionStyle("font")
        # 转化相对路径
        if ":" not in font_path:
            font_path = join(GetPath(), font_path)
        text_clip = TextClip(
            font = GetCaptionStyle("font"),
            text = text,
            font_size = fontsize,
            color = GetCaptionStyle("color"),
        ).with_position(GetCaptionStyle("position"), relative=GetCaptionStyle("relative"))
        clip_dur = clip.duration
        clip = CompositeVideoClip([clip, text_clip]).with_duration(clip_dur)
        
        return clip


def add_scoreboard(clip: VideoClip, home: int = 0, away: int = 0) -> VideoClip:
    """
    加比分牌。显示的队名通过 zxx.options.SetMatchInfo() 设置。

    参数说明：
        clip：要加比分牌的视频片段。类型是 moviepy.video 的 VideoClip 类。
        home：主队当前得分。
        away：客队当前得分。
    """
    from moviepy import ImageClip, CompositeVideoClip
    from moviepy.video import fx as vfx
    from os.path import join
    from .options import GetPath, GetMatchInfo, GetScoreBoardStyle

    # 生成比分牌文字内容
    home_name = GetMatchInfo("home")
    away_name = GetMatchInfo("away")
    text = f"{home_name}　{home}-{away}　{away_name}"
    fontpath = join(GetPath(), GetScoreBoardStyle("font_file"))
    # 合成比分牌图片
    img = add_txt_to_img_center(
        filename = GetScoreBoardStyle("image"),
        text = text,
        fontpath = fontpath,
        color = GetScoreBoardStyle("color") 
    )
    # 合成图片和视频
    clip_width = clip.size[0]
    width_factor = GetScoreBoardStyle("width_factor")
    score_width = width_factor * clip_width
    score_clip = ImageClip(img).with_effects([vfx.Resize(width=score_width)])
    # 调整比分牌显示时长
    clip_dur = clip.duration
    clip = CompositeVideoClip([clip, score_clip]).with_duration(clip_dur)

    return clip


# if __name__ == "__main__":
#     from moviepy import VideoFileClip, AudioFileClip
#     from .options import SetPath, SetScoreBoardStyle
#     SetPath("E:\\temp_video_import")
#     SetScoreBoardStyle(font_file="NotoSansSC-Bold.otf")
#     path = "E:\\temp_video_import\\片尾.mp4"
#     clip = VideoFileClip(path)
#     clip = add_scoreboard(clip=clip)
#     clip.write_videofile("E:\\temp_video_import\\片尾_test.mp4", threads=8)
