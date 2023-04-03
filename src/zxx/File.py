"""
文件类

针对文件操作
"""

from moviepy.editor import *
from os.path import join

from .options import GetPath
from .tools import str2sec
from .Video import Video

class File:
    def __init__(self, filename:str, folder:str=None):
        self.__filename = filename
        self.__folder = folder
        if folder == None:
            self.__folder = GetPath()
        self.__path = join(self.__folder, self.__filename)
        self.__contents = VideoFileClip(self.__path)

    def contents(self) -> VideoFileClip:
        """获取文件内容"""
        return self.__contents

    def select(self, begin:str, finish:str) -> "Video":
        """截取视频文件中的一段"""
        b = str2sec(begin)
        e = str2sec(finish)
        if b >= e:
            raise Exception("时间轴错误：开始时刻 %s 未能早于结束时刻 %s" % (begin, finish))
        else:
            clip = self.contents().subclip(b, e)
            video = Video(contents=clip)
        return video
