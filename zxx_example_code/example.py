"""
Python package zxx 1.0.1
Latest update: 2024-10-23

Example code 示例代码

版权声明：
    1. 背景音乐文件为开源音乐。歌曲：A Thousand Years，来自：
        https://www.fiftysounds.com/zh/
    2. 比分牌字体文件为开源字体「得意黑」，来自：
        https://github.com/atelier-anchor/smiley-sans/releases
    3. 比分版图片素材和片尾视频素材均为自制。
    4. 比赛素材为自行录制，来源于「北大杯」女足比赛，无版权问题。

说明：
    1. 由于 zxx 库依赖 moviepy 库进行视频编辑，而 moviepy 的运行需要
        首先自行安装 ImageMagick。因此在使用 zxx 库前，也需要先在电脑
        上手动安装 ImageMagick，才能正常使用。安装方式请参考：
        https://www.imagemagick.org/script/download.php
    2. 以下是一个示例代码，包含了 zxx 库的常用函数，您可以直接参考
        下面的示例代码来获知本库的使用方式。在实际使用时，只需要根
        据需要选择以下示例代码中的一部分，并加以调整即可。
    3. 如需了解各函数的参数和具体用法，请直接参考函数的 docstring，
        不再提供单独的使用指南。在主流编辑器中，可以将鼠标悬置在代
        码里的相应函数上，即可自动显示。
    4. 如果安装了 ImageMagick 后依然无法正常使用，可能需要在 moviepy
        库源代码中调整相应设置（这是 moviepy 库的固有问题），可参考：
        https://blog.csdn.net/qq_23944915/article/details/86514301，
        以及 https://blog.csdn.net/biggbang/article/details/121498690
"""


from zxx import Highlight
from zxx.options import SetPath, SetMatchInfo, SetCaptionStyle, SetScoreBoardStyle, AllFonts
from os.path import dirname, realpath


# 全局设置
my_path = dirname(realpath(__file__))    # 将当前脚本所在的路径设置为工作路径
SetPath(my_path)
SetMatchInfo(
    home = "主队队名",
    away = "客队队名",
)
AllFonts()    # 查看自己的电脑里安装了哪些字体
SetCaptionStyle(    # 设置字幕样式
    font = "包图小白体",    # 这个必须是电脑上已经安装的字体名
    color = "pink",
    position = ("right", "bottom"),
    fontsize = 70
)
SetScoreBoardStyle(    # 设置记分牌样式
    image = "scoreboard.png",    # 这个文件需要提前放到工作目录
    font_file = "SmileySans-Oblique.ttf",    # 这个文件需要提前放到工作目录
    color = "black"
)


def main():
    my_highlight = (
        Highlight()
        .show_score(True)
        .use("素材1.mp4").take(    # 素材文件需要提前放到工作目录
            ["00:06", "00:18", "我方26号球员带球突破，射门得分！"],
            ["00:13", "00:16.5", "精彩回放", {"speed": 0.5, "fadein": 1}],
        )
        .set_score(1, 0)
        .use("素材2.mp4").take(    # 素材文件需要提前放到工作目录
            ["我方26号球员前场抢断，梅开二度！", {"fadein": 1}],
        )
        .set_score(2, 0)
        .print_duration()
        .silence()
        .add_bgm(    # 背景音乐文件需要提前放到工作目录
            "A Thousand Years.mp3", select=["", "00:32"], mode="change_music_speed",
        )
        .show_score(False)
        .use("片尾.mp4").take()
        .export(
            filename = "集锦.mp4",
            # mode = "preview",    # 使用这一选项可以快速导出预览
            mode = "hd",    # 使用这一选项导出成片
        )
    )


if __name__ == "__main__":
    main()
