"""
zxx.tools
小工具
    供其他模块使用的一些工具性函数，不建议在剪辑集锦时直接调用。
"""


from moviepy import VideoClip
from PIL import Image
import numpy as np


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
    # 删去秒数的小数部分末尾多余的 0
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
        return f"00:{s}"
    
    h_f, m_f = map(int, divmod(m_f, 60))
    if h_f == 0:
        string = f"{m_f:0=2d}:{s}"
    else:
        string = f"{h_f:0=2d}:{m_f:0=2d}:{s}"

    return string


def add_effects(clip: VideoClip, speed: float = 1, duration: float | None = None, silence: bool = False, lum: float = 0, 
                contrast: float = 0, fadein: float = 0, fadeout: float = 0, crop: tuple[float, float, float, float] | None = None, 
                crop_abs: tuple[int, int, int, int] | None = None, crop_keep_ratio: tuple[float, float, float] | None = None, 
                crop_keep_ratio_abs: tuple[int, int, int] | None = None,) -> VideoClip:
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
        crop 系列参数用于裁剪视频，但注意可能导致比例失真（crop 和 crop_relative）。这四个参数只能同时指定一个。
            crop：裁切视频指定长方形区域，指定裁切区域左上角和右下角的相对位置。
                顺序也是 (x1, y1, x2, y2)，例如 (2/3, 1/3, 1, 2/3)，表示裁切区域是视频九宫格的右侧居中那格。
            crop_abs：裁切视频指定长方形区域，依次指定裁切区域左上角和右下角坐标，顺序是 (x1, y1, x2, y2)，
                以左上角为 (0, 0)。
            crop_keep_ratio：裁切视频指定长方形区域，指定裁切区域左上角坐标和右下角横坐标的相对位置。
                y2 将根据视频比例自动计算得到。
            crop_keep_ratio_abs：裁切视频指定长方形区域，依次指定裁切区域左上角坐标和右下角横坐标，
                顺序是 (x1, y1, x2)。y2 将根据视频比例自动计算得到。例如 (2/3, 1/3, 1)，
                表示裁切区域是视频九宫格的右侧居中那格。
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
    # 裁切画面
    temp_list = [crop, crop_abs, crop_keep_ratio, crop_keep_ratio_abs]
    ori_size = clip.size
    crop_cmd_num = len([item for item in temp_list if item is not None])
    if crop_cmd_num == 0:
        pass
    elif crop_cmd_num >= 2:
        raise Exception("只能同时指定`crop`系列参数中的一个噢！请重新设置参数。")
    else:
        if crop_abs is not None:
            x1, y1, x2, y2 = crop_abs
            if x2 <= x1:
                raise Exception(f"裁切选区的右边界（当前为{x2}）需大于左边界（当前为{x1}），请重新设置参数。")
            if y2 <= y1:
                raise Exception(f"裁切选区的下边界（当前为{y2}）需大于上边界（当前为{y1}），请重新设置参数。")
            clip = clip.with_effects([vfx.Crop(x1=x1, y1=y1, x2=x2, y2=y2)])
        elif crop is not None:
            video_width, video_height = clip.size
            x1, y1, x2, y2 = (int(video_width * crop[0]), int(video_height * crop[1]),
                            int(video_width * crop[2]), int(video_height * crop[3]))
            if x2 <= x1:
                raise Exception(f"裁切选区的右边界（当前为{crop[2]}）需大于左边界（当前为{crop[0]}），请重新设置参数。")
            if y2 <= y1:
                raise Exception(f"裁切选区的下边界（当前为{crop[3]}）需大于上边界（当前为{crop[1]}），请重新设置参数。")
            clip = clip.with_effects([vfx.Crop(x1=x1, y1=y1, x2=x2, y2=y2)])
        elif crop_keep_ratio_abs is not None:
            video_width, video_height = clip.size
            x1, y1, x2 = crop_keep_ratio_abs
            y2 = int(y1 + (x2 - x1) / video_width * video_height)
            if y2 > video_height:
                raise Exception("裁切选区下界超过了原视频的下界，请重新设置。")
            if x2 <= x1:
                raise Exception(f"裁切选区的右边界（当前为{x2}）需大于左边界（当前为{x1}），请重新设置参数。")
            if y2 <= y1:
                raise Exception(f"裁切选区的下边界（当前为{y2}）需大于上边界（当前为{y1}），请重新设置参数。")
            clip = clip.with_effects([vfx.Crop(x1=x1, y1=y1, x2=x2, y2=y2)])
        elif crop_keep_ratio is not None:
            video_width, video_height = clip.size
            x1, y1, x2 = (int(video_width * crop_keep_ratio[0]),
                        int(video_height * crop_keep_ratio[1]),
                        int(video_width * crop_keep_ratio[2]))
            y2 = int(y1 + (x2 - x1) / video_width * video_height)
            if y2 > video_height:
                raise Exception("裁切选区下界超过了原视频的下界，请重新设置。")
            if x2 <= x1:
                raise Exception(f"裁切选区的右边界（当前为{crop_keep_ratio[2]}）需大于左边界（当前为{crop_keep_ratio[0]}），请重新设置参数。")
            clip = clip.with_effects([vfx.Crop(x1=x1, y1=y1, x2=x2, y2=y2)])
        # 用原始分辨率重写视频
        clip = clip.with_effects([vfx.Resize(ori_size)])
    return clip


def draw_round_rect(width: float, height: float, r: float, color: str | tuple | None = None) -> np.ndarray:
    """
    创建一个圆角矩形。

    参数说明：
        width：矩形的宽度。
        height：矩形的高度。
        r：圆角半径。
    """
    from PIL import Image, ImageDraw
    import numpy as np
    
    board_size = (width, height)
    img = Image.new(mode="RGBA", size=board_size, color=None)
    draw = ImageDraw.Draw(img)
    # 圆角
    draw.ellipse((0, 0, r, r), fill=color)
    draw.ellipse((width - r, 0, width, r), fill=color)
    draw.ellipse((0, height - r, r, height), fill=color)
    draw.ellipse((width - r, height - r, width, height),fill=color)
    # 矩形
    draw.rectangle((r/2, 0, width - (r/2), height), fill=color)
    draw.rectangle((0, r/2, width, height - (r/2)), fill=color)
    img_array = np.array(img)
    return img_array


def __make_caption_clip(clip: VideoClip, text: str) -> VideoClip:
    """
    生成字幕 clip，参数参见 add_caption() 方法。
    """
    from moviepy import TextClip, CompositeVideoClip, ImageClip
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
    # 生成文字
    background = GetCaptionStyle("background")
    if background is None:
        text_clip = TextClip(
            font = font_path,
            text = text,
            font_size = fontsize,
            color = GetCaptionStyle("color"),
        ).with_position(GetCaptionStyle("position"), relative=GetCaptionStyle("relative"))
    else:
        # 加背景。不直接使用 TextClip 的 bg_color 参数是因为这一选项不提供圆角矩形的背景，
        # 也不能微调字幕的具体位置
        text_clip_sample = TextClip(font=font_path, text=text, font_size=fontsize)
        m = GetCaptionStyle("margin")
        v_adj = GetCaptionStyle("vertical_adj")
        rect_w, rect_h = [l + 2 * m for l in text_clip_sample.size]
        r = rect_h / 3
        img_array = draw_round_rect(rect_w, rect_h, r, background)
        bg_clip = ImageClip(img_array)
        v_start = (rect_h - text_clip_sample.size[1]) / 2 - v_adj    # 调整字体的垂直位置
        text_clip = TextClip(
            font = font_path,
            text = text,
            font_size = fontsize,
            color = GetCaptionStyle("color"),
        ).with_position(("center", v_start))
        text_clip = (
            CompositeVideoClip([bg_clip, text_clip])
            .with_position(GetCaptionStyle("position"), relative=GetCaptionStyle("relative"))
        )

    return text_clip


def add_caption(clip: VideoClip, text: str) -> VideoClip:
    """
    给视频片段加字幕。
    字幕的字体、字号、颜色、位置等参数，通过 zxx.options.SetCaptionStyle() 统一设置。

    参数说明：
        clip：要加字幕的视频片段。类型是 moviepy.video 的 VideoClip 类。
        text：字幕文案。可以为空字符串。
    """
    from moviepy import CompositeVideoClip

    clip_dur = clip.duration
    text_clip = __make_caption_clip(clip, text)
    clip = CompositeVideoClip([clip, text_clip]).with_duration(clip_dur)

    return clip


def draw_dufault_scoreboard_picture(color: str | tuple) -> Image.Image:
    """
    绘制默认的记分牌。
    """
    from PIL import Image, ImageDraw

    # 画六边形（切角的矩形）
    board_size = (1969, 303)
    img = Image.new(mode="RGBA", size=board_size, color=None)
    polygon_vertices = [(139, 31), (1944, 31), (1944, 150), (1832, 262), (27, 262), (27, 143)]
    draw = (
        ImageDraw.Draw(img)
        .polygon(xy=polygon_vertices, fill=color)
    )
    # 画阴影
    final = Image.new("RGBA", size=board_size, color=None)
    max_offset = 19
    max_alpha = 0xcc
    left_bottom_side = polygon_vertices[3:6]    # 描出六边形的左边和下边
    for offset in range(1, max_offset + 1):
        offset_x, offset_y = -offset, offset    # 逐渐往左下角偏移
        shadow_canvas = Image.new(mode="RGBA", size=board_size, color=None)
        alpha = int(max_alpha * (1 - (offset - 1) / max_offset) ** 0.5)   # 非线性的渐变透明度
        shadow_color = f"#000000{alpha:02x}"
        shifted_lines = [(x + offset_x, y + offset_y) for x, y in left_bottom_side]    # 描阴影线
        draw = ImageDraw.Draw(shadow_canvas)
        draw.line(xy=shifted_lines, fill=shadow_color, width=1)
        final.paste(shadow_canvas, (0, 0), shadow_canvas)
    final.paste(img, (0, 0), img)
    return final


def add_txt_to_img_center(text: str, fontpath: str, color: str | tuple, fontsize_factor: float, 
                          filename: str | None = None, img_pil: Image.Image | None = None) -> Image.Image:
    """
    在图片正中央添加文字。

    参数说明：
        text：要加的文字。
        fontpath：字体文件的路径，注意是绝对路径。
        color：字体颜色，参数值会直接传送给 PIL.ImageDraw.text() 方法的 fill 参数，
            使用色彩名、十六进制、RGB、RGBA 等均可，可采用以下写法中的任意一种：
                color="pink"
                color="#800080"
                color=(255, 10, 10)
                color=(255, 10, 10, 100)
        fontsize_factor：字体大小最多占据图片高度或宽度的多少，范围在 0-1 之间。
        filename：要加字的图片文件名，工作路径（即 zxx.options.GetPath() 返回值）的相对路径。会覆盖 img_pil 的设置。
        img_pil：以 PIL.Image.Image 对象格式传入的图片。
    """
    import cv2
    from PIL import ImageFont, ImageDraw, Image
    import numpy as np
    from os.path import join
    from .options import GetPath

    if filename is not None:
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
    font_base = ImageFont.truetype(fontpath, 100)
    x_0b, y_0b, x_1b, y_1b = font_base.getbbox(text)    # 获取边界框
    font_base_width, font_base_height = abs(x_1b - x_0b), abs(y_1b - y_0b)
    max_text_width, max_text_height = fontsize_factor * width, fontsize_factor * height
    factor_on_base = min(max_text_width / font_base_width, max_text_height / font_base_height)
    fontsize = int(factor_on_base * 100)
    font = ImageFont.truetype(fontpath, fontsize)

    # 精确处理文字位置（居中）
    x_0, y_0, x_1, y_1 = font.getbbox(text)
    position = ((width - x_1 - x_0) / 2, (height - y_1 - y_0) / 2)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=color)
    img = np.array(img_pil)

    return img


def __make_scoreboard_clip(clip: VideoClip, home: int = 0, away: int = 0) -> VideoClip:
    """
    生成比分牌 clip，参数参见 add_scoreboard() 方法。
    """
    from moviepy import ImageClip
    from moviepy.video import fx as vfx
    from os.path import join
    from .options import GetPath, GetMatchInfo, GetScoreBoardStyle

    # 生成比分牌文字内容
    home_name = GetMatchInfo("home")
    away_name = GetMatchInfo("away")
    text = f"{home_name}　{home}-{away}　{away_name}"
    fontpath = join(GetPath(), GetScoreBoardStyle("font_file"))
    # 合成比分牌图片
    filename = GetScoreBoardStyle("image")
    img_pil = None
    if filename is None:
        board_color = GetScoreBoardStyle("board_color")
        img_pil = draw_dufault_scoreboard_picture(color=board_color)
    img = add_txt_to_img_center(
        text = text,
        fontpath = fontpath,
        color = GetScoreBoardStyle("color"),
        fontsize_factor = GetScoreBoardStyle("fontsize_factor"),
        filename = GetScoreBoardStyle("image"),
        img_pil = img_pil,
    )
    # 合成图片和视频
    clip_width = clip.size[0]
    width_factor = GetScoreBoardStyle("width_factor")
    score_width = width_factor * clip_width
    score_clip = (
        ImageClip(img)
        .with_effects([vfx.Resize(width=score_width)])
        .with_position(GetScoreBoardStyle("position"), relative=GetScoreBoardStyle("relative"))
    )
    return score_clip


def add_scoreboard(clip: VideoClip, home: int = 0, away: int = 0) -> VideoClip:
    """
    加比分牌。显示的队名通过 zxx.options.SetMatchInfo() 设置。

    参数说明：
        clip：要加比分牌的视频片段。类型是 moviepy.video 的 VideoClip 类。
        home：主队当前得分。
        away：客队当前得分。
    """
    from moviepy import CompositeVideoClip

    score_clip = __make_scoreboard_clip(clip, home, away)
    clip_dur = clip.duration
    clip = CompositeVideoClip([clip, score_clip]).with_duration(clip_dur)
    return clip


def add_caption_and_scoreboard(clip: VideoClip, text: str, home: int = 0, away: int = 0) -> VideoClip:
    """
    同时加字幕和比分牌。参数参见 add_scoreboard() 和 add_caption() 方法。
    """
    from moviepy import CompositeVideoClip

    clip_dur = clip.duration
    text_clip = __make_caption_clip(clip, text)
    score_clip = __make_scoreboard_clip(clip, home, away)
    clip = CompositeVideoClip([clip, score_clip, text_clip]).with_duration(clip_dur)

    return clip



if __name__ == "__main__":
    draw_round_rect(1000, 500, 200, "#00000020")

