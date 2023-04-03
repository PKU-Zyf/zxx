"""
视频类

对某个片段进行内部处理，不涉及裁剪和拼接等
"""

from moviepy.editor import *
from os import path

from .options import GetPath, GetMatchInfo, GetCaptionStyle, GetScoreBoardStyle
from .tools import sec2str, add_txt_to_img_center

class Video():
    def __init__(self, contents:VideoClip=None):
        self.__contents = contents

    # 以下方法返回的不是 self，而是一些参数

    def contents(self):
        """获取视频内容"""
        return self.__contents

    def length(self):
        """获取视频时长"""
        dur = sec2str(self.contents().duration)
        return dur
    
    # 以下方法返回的是 self，可用于链式写法

    def print_length(self):
        """打印视频时长"""
        print(self.length())
        return self
    
    def effects(self, speed:float=1, silence:bool=False, lum:float=0, 
                contrast:float=0, fadein:float=0, fadeout:float=0):
        """视频特效"""
        clip = self.contents()
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
        self.__contents = clip
        return self

    def caption(self, text:str):
        """加字幕"""
        clip = self.contents()
        text_clip = TextClip(
            text,
            font     = GetCaptionStyle("font"),
            fontsize = GetCaptionStyle("fontsize"),
            color    = GetCaptionStyle("color"),
        ).set_position(GetCaptionStyle("position"))
        clip_dur = clip.duration
        clip = CompositeVideoClip([clip, text_clip]).set_duration(clip_dur)
        self.__contents = clip
        return self
    
    def scoreboard(self, home:int=0, away:int=0):
        """加比分牌"""
        clip = self.contents()
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
        self.__contents = clip
        return self

    def export(self, filename:str, folder:str=None, mode:str="hd"):
        """导出视频文件"""
        if folder == None:
            folder = GetPath()
        output_path = path.join(folder, filename)
        # 快速导出
        # 视频文件会很小，可以使用 mp4 格式
        if mode == "preview":
            self.__contents.write_videofile(
                output_path,
                fps = 24,
                preset = "ultrafast",
                bitrate = "1000k",
            )
        # 高清画质
        # 视频压缩效果好，对应格式为 mp4，视频质量通过 bitrate 参数调节
        elif mode == "hd":
            self.__contents.write_videofile(
                output_path,
                codec = "libx264",
                bitrate = "20000k",    # B站推荐4k视频码率大于20000kbps
            )
        # 无损画质
        # 完美的视频质量，对应格式为 avi，文件比较大
        elif mode == "lossless":
            self.__contents.write_videofile(
                output_path,
                codec = "png",
                bitrate = "20000k",
            )
        print("视频已导出至 %s" % output_path)
        return self
 