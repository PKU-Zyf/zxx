"""
集锦类

"""

from moviepy.editor import *
from os import path

from .File import File
from .options import GetPath
from .tools import str2sec, sec2str
from .Video import Video

class Highlight():
    def __init__(self, contents:VideoClip=None):
        self.__contents = contents
        self.__source_file = None
        self.__score = (0, 0)
        self.__show_score = False

    # 以下方法和 Vedio() 一样

    def contents(self):
        """获取视频内容"""
        return self.__contents

    def length(self):
        """获取视频时长"""
        dur = sec2str(self.contents().duration)
        return dur
    
    def print_length(self):
        """打印视频时长"""
        print(self.length())
        return self

    # 以下是 Highlight 类的独有方法

    def source_file(self):
        return self.__source_file
    
    def score(self):
        return self.__score

    def add_video(self, video: "Video"):
        """向集锦中追加一段视频"""
        if self.contents() == None:
            self.__contents = video.contents()
        else:
            self.__contents = concatenate_videoclips([self.contents(), video.contents()])
        return self
    
    def silence(self):
        """消音"""
        clip = self.contents()
        self.__contents = clip.without_audio()
        return self

    def add_bgm(self, filename: str, folder: str = None, 
                select: list = [], repeat: int = 1, mode = "cut"):
        if folder == None:
            folder = GetPath()
        video_clip = self.__contents
        audio_clip = AudioFileClip(path.join(folder, filename))
        if select != []:
            b = str2sec(select[0])
            e = str2sec(select[1])
            if b >= e:
                raise Exception("背景音乐剪辑错误：开始时间（%s）不早于结束时间（%s）" % (b, e))
            else:
                audio_clip = audio_clip.subclip(b, e)
        if repeat > 1:
            for i in range(repeat - 1):
                audio_clip = concatenate_audioclips([audio_clip, audio_clip])
        video_duration = video_clip.duration
        audio_duration = audio_clip.duration
        if mode == "cut":               # 视频结束停止音乐
            audio_clip = audio_clip.subclip(0, video_duration)
            self.__contents = video_clip.set_audio(audio_clip)
        elif mode == "change_speed":    # 调整音乐速度，匹配视频时长
            speed = audio_duration / video_duration
            audio_clip = audio_clip.fl_time(lambda t:speed*t)
            audio_clip = audio_clip.set_duration(audio_duration / speed)
            self.__contents = video_clip.set_audio(audio_clip)
            print("为匹配视频长度，背景音乐速度已调整为原先的 %.2f 倍" % speed)
        else:
            print("添加背景音乐失败，请指定模式（\"cut\" 或 \"change_speed\"）" % speed)
        return self
    
    def volume_normalize(self):
        """标准化音量
        
        不过现在还有点问题
        """
        clip = self.contents()
        self.__contents = clip.audio_normalize()
        return self
    
    # 以下几个函数可连环使用，用于精简流程

    def use(self, filename:str, folder:str=None):
        """指定接下来使用的视频文件"""
        self.__source_file = File(filename, folder)
        return self
    
    def show_score(self, show:bool=True):
        """设置是否显示比分"""
        self.__show_score = show
        return self
    
    def set_score(self, home:int, away:int):
        """更新比分"""
        self.__score = (home, away)
        return self
    
    def take(self, *args:list):
        """指定从正在使用的视频文件中提取剪辑的相关信息
        
        每个 list 按照如下顺序排列：
            [起始时刻str, 结束时刻str, 字幕str, 特效dict]
            后两个可选
        """
        for info in args:
            begin = info[0]
            end = info[1]
            vedio = self.source_file().select(begin, end)
            # 先加特效，再加字幕和比分牌
            if len(info) == 4:
                effects = info[3]
                vedio.effects(**effects)
                caption = info[2]
                vedio.caption(caption)
            if len(info) == 3:
                if isinstance(info[2], dict):
                    effects = info[2]
                    vedio.effects(**effects)
                else:
                    caption = info[2]
                    vedio.caption(caption)
            if self.__show_score:
                home_score, away_score = self.score()
                vedio.scoreboard(home_score, away_score)
            self.add_video(vedio)
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
 
    

    

