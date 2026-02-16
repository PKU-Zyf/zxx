"""
Python package zxx 1.3.0
Latest update: 2026-02-17

后续有待解决的事项：
    1. 添加多个BGM
        - 附加一个（分别）标准化音量的功能，使用 moviepy.audio.fx.AudioNormalize
        - 音乐的渐强渐弱 moviepy.audio.fx.AudioFadeIn / AudioFadeOut
    2. 内存管理问题。似乎没有特别好的办法，可能需要指导用户临时增加虚拟内存。
    3. 视频增稳 moviepy.video.io.ffmpeg_tools.ffmpeg_stabilize_video
    4. 管理实例中所有打开的 clip，集中关闭（修复“OSError: [WinError 6] 句柄无效”提醒）
"""


from .File import File
from .Highlight import Highlight
