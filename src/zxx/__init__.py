"""
Python package zxx 1.1.0
Latest update: 2025-07-30

各模块调用顺序：
    Highlight <- File <- tools <- options

后续有待解决的事项：
    1. 可以增加一个标准化音量的功能。
    2. SetCaptionStyle() 和 SetScoreBoardStyle() 指定字体属性的方式不一样，一个是基于 ImageMagick，一个是基于 Pillow，使用起来不统一。
"""


from .File import File
from .Highlight import Highlight
