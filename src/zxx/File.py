"""
zxx.File
文件类
    针对外部的视频或音频文件进行基本操作。
"""


from __future__ import annotations
from moviepy.editor import *
from os.path import join

from .options import GetPath
from .tools import str2sec


class File:
    def __init__(self, filename: str, folder: str = None) -> None:
        """
        zxx.File 文件类，针对外部的视频或音频文件进行基本操作。

        参数说明：
            filename：新建 zxx.File 类的一个实例时，必须指定文件名。文件名是相对于 folder 的相对路径。
            folder：视频文件所在的文件夹绝对路径。如果未指定，则默认为工作目录（即 zxx.options.GetPath() 的返回值）。
        """
        self.__filename = filename
        self.__folder = folder
        if folder == None:
            self.__folder = GetPath()
        self.__path = join(self.__folder, self.__filename)
        self.__contents = VideoFileClip(self.__path)

    def contents(self) -> VideoFileClip:
        """
        获取文件内容。返回值类型是 moviepy.video.io 的 VideoFileClip 类。
        """
        return self.__contents

    def select(self, begin: str, finish: str) -> VideoClip:
        """
        截取视频文件中的一段，并根据这段内容生成 moviepy.video 的 VideoClip 类的一个实例。

        参数说明：
            begin：开始时间点，可以写成 "1:03:13" 这样的形式。
            finish：结束时间点，写法同上。注意开始时刻必须早于结束时刻。
        """
        b = str2sec(begin)
        e = str2sec(finish)
        if b >= e:
            raise Exception("时间轴错误：开始时刻 %s 未能早于结束时刻 %s" % (begin, finish))
        else:
            clip = self.contents().subclip(b, e)
        return clip
