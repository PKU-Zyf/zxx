# zxx
# 最后更新：2022-11-07

from os import path
from moviepy.editor import *

PATH = path.dirname(path.realpath(__file__))

# 字符串转秒数
def str2sec(string):
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
    seconds = 3600 * int(h) + 60 * int(m) + int(s)
    return seconds

# 依次拼接视频
def join_videos(*videos: "Video"):
    video = videos[0]
    for i in range(1, len(videos)):
        video.add(videos[i])
    return video

class Video:
    def __init__(self, filename="test.mp4", folder=PATH):
        self.__folder = folder
        self.__filename = filename
        self.__path = path.join(self.__folder, self.__filename)
        self.__contents = VideoFileClip(self.__path)

    def contents(self):
        return self.__contents

    # 选取片段
    def select(self, begin_point: str, finish_point: str):
        clip = self.__contents.subclip(
            str2sec(begin_point),
            str2sec(finish_point),
        )
        return clip

    # 剪辑
    def cut(self, *timeline: list):
        clips = []
        for time_range in timeline:
            clip = self.select(time_range[0], time_range[1])
            clips.append(clip)
        self.__contents = concatenate_videoclips(clips)
        return self

    # 剪辑并加字幕
    def cut_with_text(self, *timeline: list):
        my_clips = []
        for info in timeline:
            duration = str2sec(info[1]) - str2sec(info[0])
            txt = info[2]
            vedio_clip = self.select(info[0], info[1])
            text_clip = TextClip(
                txt,
                font = "包图小白体",
                fontsize = 100,    # 一行大约19个字
                color = "white",
            ).set_position("bottom")
            clip = CompositeVideoClip([vedio_clip, text_clip]).set_duration(duration)
            my_clips.append(clip)
        self.__contents = concatenate_videoclips(my_clips)
        return self

    # 追加一段视频
    def add(self, video: "Video"):
        self.__contents = concatenate_videoclips([self.__contents, video.contents()])
        return self

    # 消音
    def silence(self):
        self.__contents = self.__contents.without_audio()
        return self

    # 配音
    def add_bgm(self, filename="bgm.mp3", folder=PATH, mode="cut"):
        audio_clip = AudioFileClip(path.join(folder, filename))
        video_duration = self.__contents.duration
        audio_duration = audio_clip.duration
        if mode == "cut":    # 视频结束停止音乐
            audio_clip = audio_clip.subclip(0, video_duration)
            self.__contents = self.__contents.set_audio(audio_clip)
        elif mode == "change_speed":    # 调整音乐速度，匹配视频时长
            speed = audio_duration / video_duration
            audio_clip = audio_clip.fl_time(lambda t:speed*t)
            audio_clip = audio_clip.set_duration(audio_duration / speed)
            self.__contents = self.__contents.set_audio(audio_clip)
            print("为匹配视频长度，背景音乐速度已调整为原先的 %.2f 倍" % speed)
        else:
            print("添加背景音乐失败，请指定模式（\"cut\" 或 \"change_speed\"）" % speed)
        return self

    # 导出视频文件
    def export(self, filename="output.avi", folder=PATH, mode="hd"):
        output_path = path.join(folder, filename)
        if mode == "preview":       # 快速导出
            self.__contents.write_videofile(
                output_path,
                fps = 24,
                preset = "ultrafast",
                bitrate = "1000k",
            )
        elif mode == "hd":          # 高清画质
            self.__contents.write_videofile(
                output_path,
                codec = "libx264",
                bitrate = "20000k",    # B站推荐4k视频码率大于20000kbps
            )
        elif mode == "lossless":    # 无损画质
            self.__contents.write_videofile(
                output_path,
                codec = "png",
                bitrate = "20000k",
            )
        print("视频已导出至 %s" % output_path)
        return self
