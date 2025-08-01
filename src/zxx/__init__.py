"""
Python package zxx 1.2.0
Latest update: 2025-08-01

各模块调用顺序：
    Highlight <- File <- tools <- options

后续有待解决的事项：
    1. 添加多个BGM
        - 附加一个（分别）标准化音量的功能，使用 moviepy.audio.fx.AudioNormalize
        - 音乐的渐强渐弱 moviepy.audio.fx.AudioFadeIn / AudioFadeOut
    2. 内存管理问题。
    3. 视频增稳 moviepy.video.io.ffmpeg_tools.ffmpeg_stabilize_video
"""


from .File import File
from .Highlight import Highlight
