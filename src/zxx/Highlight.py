"""
zxx.Highlight
集锦类
    由视频片段处理组合形成的视频集锦。
"""


from __future__ import annotations
from moviepy.editor import *
from os import path

from .options import GetPath, SetMatchInfo
from .tools import str2sec, sec2str, add_effects, add_caption, add_scoreboard
from .File import File


class Highlight():
    def __init__(self, contents: VideoClip = None):
        """
        zxx.Highlight 集锦类，由多个经过处理的视频片段组合形成集锦，并对集锦进行配置背景音乐、刷新比分等进一步操作。

        参数说明：
            contents：集锦的初始内容，类型是 moviepy.video 的 VideoClip 类。新建集锦实例时，建议不指定 contents。
        """
        self.__contents = contents
        self.__source_file = None
        self.__score = (0, 0)
        self.__show_score = False

    # 以下方法和 zxx.Vedio 类是一样的

    def contents(self) -> VideoClip | None:
        """
        获取视频内容。
        """
        return self.__contents

    def duration(self) -> str:
        """
        获取视频时长。
        """
        dur = sec2str(self.contents().duration)
        return dur

    def print_duration(self) -> Highlight:
        """
        打印视频时长。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。
        """
        print(self.duration())
        return self

    # 以下是 Highlight 类独有的方法

    def source_file(self) -> File:
        """
        返回集锦当前正在处理的视频片段的源文件，类型为 zxx.File。
        """
        return self.__source_file

    def score(self) -> tuple:
        """
        返回当前比分（主队得分在前）。
        """
        return self.__score

    def __add_video(self, clip: VideoClip) -> Highlight:
        """
        【不建议外部调用本方法，实际剪辑集锦时，应使用 zxx.Highlight.use() 代替】

        向集锦中追加一段视频片段。如果新追加视频画面尺寸不同，会自动将新视频统一成和已有集锦相同的尺寸。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。

        参数说明：
            video：要追加的视频片段，类型是 moviepy.video 的 VideoClip 类。
        """
        if self.contents() == None:
            self.__contents = clip
        else:
            # 统一视频尺寸
            hl_size = self.__contents.size
            v_size = clip.size
            if hl_size != v_size:
                new_clip = clip.resize(hl_size)
            else:
                new_clip = clip
            self.__contents = concatenate_videoclips([self.contents(), new_clip])
        return self

    def silence(self) -> Highlight:
        """
        集锦整体消音。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。
        """
        clip = self.contents()
        self.__contents = clip.without_audio()
        return self

    def add_bgm(self, filename: str, folder: str = None, 
                select: list = [], repeat: int = 1, mode = "cut") -> Highlight:
        """
        为集锦添加背景音乐。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。

        参数说明：
            filename：背景音乐的文件名。
            folder：背景音乐文件所在的文件夹绝对路径。如果未指定，则默认为工作目录（即 zxx.options.GetPath() 的返回值）。
            select：选择截取音乐的时间范围。
                写成 ["02:12", "03:06"] 这样的形式。注意开始时刻必须早于结束时刻。
                开始 / 结束时刻如果是空字符串，默认是音乐的开始 / 结束处。
            repeat：设置把截取的音乐片段重复几次（默认为 1，即不重复）
            mode：设置配乐的模式。具体有如下选择：
                mode = "cut"：原速播放音乐，视频结束就停止音乐。
                mode = "change_music_speed"：自动调整音乐速度，以匹配视频时长。可能导致音乐变调。
        """
        if folder == None:
            folder = GetPath()
        video_clip = self.__contents
        audio_clip = AudioFileClip(path.join(folder, filename))
        if select != []:
            if select[0] == "":
                b = 0
            else:
                b = str2sec(select[0])
            if select[1] == "":
                e = audio_clip.duration
            else:
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
        elif mode == "change_music_speed":    # 调整音乐速度，匹配视频时长
            speed = audio_duration / video_duration
            audio_clip = audio_clip.fl_time(lambda t:speed*t)
            audio_clip = audio_clip.set_duration(audio_duration / speed)
            self.__contents = video_clip.set_audio(audio_clip)
            print("为匹配视频长度，背景音乐速度已调整为原先的 %.2f 倍" % speed)
        else:
            raise Exception("添加背景音乐失败，请指定模式（\"cut\" 或 \"change_music_speed\"）")
        return self

    def use(self, filename: str, folder: str = None) -> Highlight:
        """
        指定集锦的下一段视频片段使用的视频源文件。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。
        
        参数说明：
            filename：视频文件名。
            folder：视频源文件所在的文件夹绝对路径。如果未指定，则默认为工作目录（即 zxx.options.GetPath() 的返回值）。
        """
        self.__source_file = File(filename, folder)
        return self

    def show_score(self, show: bool = True) -> Highlight:
        """
        设置是否显示比分牌。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。
        """
        self.__show_score = show
        return self

    def set_score(self, home: int, away: int) -> Highlight:
        """
        更新比分。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。

        参数说明：
            home：更新后的主队得分。
            away：更新后的客队得分。
        """
        self.__score = (home, away)
        return self

    def take(self, *args: list) -> Highlight:
        """
        从正在使用的视频中提取片段，并指定后期处理选项，然后添加至集锦的末尾。
        如果新追加视频画面尺寸不同，会自动将新视频转化成和已有集锦相同的尺寸。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。
        
        这一方法的参数是 *args，即可以传入任意数量的参数。具体用法如下：

            1. 如果不传入任何参数，则将当前正在使用的视频不作任何剪辑或后期处理，直接添加至集锦的末尾。
            2. 如果传入参数，每个参数必须是 list。每个 list 传递从视频文件中截取的一个片段和对应的后期处理信息。
            3. 每个 list 内部元素数量必须是 1 至 4 个：
                (a) 如果是 1 个字符串元素，则代表将当前正在使用的视频不作任何剪辑，只添加字幕，然后添加至集锦的末尾。例如：
                    Highlight().use("素材.mp4").take(["这是一段解说文字！"])
                (b) 如果是 1 个字典元素，则代表将当前正在使用的视频不作任何剪辑，只添加特效，然后添加至集锦的末尾。例如：
                    Highlight().use("素材.mp4").take([{"speed": 0.5, "fadein": 0.2}])
                (c) 如果是 2 个字符串元素，必须是起始时刻和结束时刻，代表将当前正在使用的视频按照该时间范围进行剪辑，不添加任何字幕或特效，然后添加至集锦的末尾。开始 / 结束时刻如果是空字符串，默认是视频的开始 / 结束处。例如：
                    Highlight().use("素材.mp4").take(["00:06", "00:20"])
                    Highlight().use("素材.mp4").take(["", "00:20"])
                    Highlight().use("素材.mp4").take(["00:06", ""])
                (d) 如果是 2 个元素，也可以按照先字幕、后特效的顺序指定，例如：
                    Highlight().use("素材.mp4").take(["这是一段解说文字！", {"speed": 0.5, "fadein": 0.2}])
                (e) 如果是 3 个元素，前 2 个元素必须是起始时刻和结束时刻，第 3 个元素是字幕或特效。例如：
                    Highlight().use("素材.mp4").take(["00:06", "00:20", "这是一段解说文字！"])
                    Highlight().use("素材.mp4").take(["00:06", "", {"speed": 0.5, "fadein": 0.2}])
                (f) 如果是 4 个元素，必须按照起始时刻、结束时刻、字幕、特效的顺序排列。例如：
                    Highlight().use("素材.mp4").take(["00:06", "", "这是一段解说文字！", {"speed": 0.5, "fadein": 0.2}])
            4. 特效元素（dict 类型）会传递到 zxx.tools.effects() 方法作为参数。
                每种特效的键名、值类型和默认值分别为：
                    speed: float = 1, 
                    silence: bool = False, 
                    lum: float = 0, 
                    contrast: float = 0, 
                    fadein: float = 0, 
                    fadeout: float = 0,
                具体意义：
                    speed：调整视频的速度倍数，不建议放慢太多，可能导致时间轴错误。
                    silence：是否消音。
                    lum：亮度要增加或减少的值，大小没有限制，不过一般在 -127 至 127 之间，可自行调试。
                    contrast：对比度要调整的值，大小没有限制，不过一般在 -1 至 1之间，可自行调试。
                    fadein：淡入效果持续的秒数。
                    fadeout：淡出效果持续的秒数。
        """
        # 不传入任何参数的情况
        if len(args) == 0:
            args = [["", ""]]
        # 分析参数
        for info in args:
            if len(info) >= 5:
                raise Exception("*args 中某一项包含元素过多，必须是 1 至 4 个！")
            if len(info) == 1:    # 处理只传入 1 个元素的情况
                info = ["", "", info[0]]
            elif len(info) == 2:    # 处理传入 2 个元素为字幕和特效的情况
                if isinstance(info[1], dict):
                    info = ["", "", info[0], info[1]]
            begin = info[0]
            end = info[1]
            if begin == "":
                begin = "0"
            if end == "":
                end = str(self.source_file().contents().duration)
            clip = self.source_file().select(begin, end)
            if len(info) == 4:    # 添加特效和字幕，顺序是先加特效，再加字幕和比分牌
                effects = info[3]
                clip = add_effects(clip, **effects)
                caption = info[2]
                clip = add_caption(clip, caption)
            elif len(info) == 3:    # 只添加特效或字幕
                if isinstance(info[2], dict):
                    effects = info[2]
                    clip = add_effects(clip, **effects)
                else:
                    caption = info[2]
                    clip = add_caption(clip, caption)
            if self.__show_score:
                home_score, away_score = self.score()
                clip = add_scoreboard(clip, home_score, away_score)
            self.__add_video(clip)
        return self

    def export(self, filename: str, folder: str = None, mode: str = "hd", threads: int | None = None) -> Highlight:
        """
        将整个集锦导出成视频文件。
        返回值是 self，即调用该函数的实例本身，因此可用于链式写法。

        参数说明：
            filename：导出的视频文件名。
            folder：导出的视频文件所在的文件夹绝对路径。如果未指定，则默认为工作目录（即 zxx.options.GetPath() 的返回值）。
            mode：导出模式。可设置以下模式：
                mode = "preview"：用于导出快速预览，视频文件会很小，建议导出文件名选择 .mp4 后缀。
                mode = "hd"：高清画质，视频压缩效果好，建议导出文件名选择 .mp4 后缀。
                mode = "DJI Action 4"：匹配大疆 Action 4 画质，建议导出文件名选择 .mp4 后缀。
                mode = "lossless"，无损画质，文件非常大，不推荐使用。建议导出文件名选择 .avi 
            threads：导出时的线程数，默认为 None 即不使用多线程。
        """
        if folder == None:
            folder = GetPath()
        output_path = path.join(folder, filename)
        # 快速导出
        if mode == "preview":
            self.__contents.write_videofile(
                output_path,
                fps = 24,
                preset = "ultrafast",
                bitrate = "1000k",
                threads = threads,
            )
        # 高清画质
        ## 视频质量通过 bitrate 参数调节，B站推荐4k视频码率大于20000kbps
        elif mode == "hd":
            self.__contents.write_videofile(
                output_path,
                codec = "libx264",
                bitrate = "20000k",
                threads = threads,
            )
        # 匹配大疆 Action 4 画质
        elif mode == "DJI Action 4":
            self.__contents.write_videofile(
                output_path,
                fps = 60,
                codec="libx264",
                bitrate="100000k",
                threads = threads,
            )
        # 无损画质
        elif mode == "lossless":
            self.__contents.write_videofile(
                output_path,
                codec = "png",
                bitrate = "20000k",
                threads = threads,
            )
        print("视频已导出至 %s" % output_path)
        return self
    
    def change_match_info(self, home: str = "", away: str = "") -> Highlight:
        """
        中途修改比赛信息（主客队信息），用于制作多场比赛的集锦。
        """
        if home != "" and away != "":
            SetMatchInfo(home=home, away=away)
        elif home != "":
            SetMatchInfo(home=home)
        elif away != "":
            SetMatchInfo(away=away)
        return self
