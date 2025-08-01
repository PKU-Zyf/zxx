# zxx

* 北京大学政信社（政信信）女足开发的 Python 库，主要用于剪辑比赛集锦。 / A Python package developed by “Zheng-Xin-She” (formerly “Zheng-Xin-Xin”) Women’s Football Team at Peking University, mainly used for editing game highlights.
* 点击[此处](https://github.com/PKU-Zyf/zxx)前往 `zxx` 的 GitHub 主页。您可以在 `zxx_example_code` 文件夹查看示例代码。 / Click [here](https://github.com/PKU-Zyf/zxx) to go to the GitHub homepage of  `zxx`. You can check example code in the  `zxx_example_code` folder.
* 点击[此处](https://pypi.org/project/zxx)前往 `zxx` 的 PyPI 主页。 / Click [here](https://pypi.org/project/zxx) to go to the PyPI homepage of `zxx`.
* 安装 / To install: `pip install zxx`.
* 更新 / To update: `pip install --upgrade zxx` / `pip install -U zxx`.
* 随着 `zxx` 库依赖的 `moviepy` 库的版本大更，现在**无需**预先安装 ImageMagick，也可正常使用。 / With a major update of the `moviepy` library, which the `zxx` library depends on, it is now **unnecessary** to install ImageMagick in advance.

## 更新日志 Update Logs

* 0.1.0 (2022-11-07)
  * 第一次正式发布。 / The first release.
* 0.2.0 (2023-04-03)
  * 全面修改运行逻辑。 / An entire modification.
* 1.0.0 (2024-10-23)
  * 修复了一些 bug，简化了使用逻辑，添加了详细的文档字符串（使用说明）。 / Fixed some bugs, simplified the usage, and added detailed docstrings.
* 1.0.1 (2024-10-23)
  * 修改了一些文字错误，增加了示例代码。 / Fixed some typos and added example code.
* 1.1.0 (2025-07-30)
  * 增加了修改主客队信息的 change_match_info() 方法。 / Add `change_match_info()` method.
  * 增加了多线程导出集锦的选项。 / Add multi-threading exporting option.
* 1.2.0 (2025-08-01)
  * 由于 `moviepy` 库版本大更至 `2.x`： / Due to the major update of the `moviepy` library to version `2.x`:
    * 不再需要预先安装 ImageMagick 了。 / Pre-installation of ImageMagick is no longer required.
    * 弃用 `tools.AllFonts()` 方法。 / The `tools.AllFonts()` method has been deprecated.
    * 全面修改了其他相关代码。 /  Other related code has been completely modified.
  * 统一比分牌和字幕的字体指定方式，兼容绝对路径和相对路径。 / Unified the font specification methods for scoreboards and subtitles, compatible with both absolute and relative paths.
  * 优化 `print_duration()` 的输出格式。 / Optimized the output format of `print_duration()`.
  * 修复视频变速时音频不同步问题。 / Fixed audio desynchronization issues during video speed adjustment.
  * 增加设置比分牌宽度的选项 `SetCaptionStyle("width_factor": 0.25)` / Added an option to set the scoreboard width: `SetCaptionStyle("width_factor": 0.25)`
  * 修改 "DJI Action 4" 导出选项帧率为 59.94（原来是 60）。 / Changed the "DJI Action 4" export frame rate from 60 to 59.94.
