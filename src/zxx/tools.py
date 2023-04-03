"""
小工具

"""

import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from .options import GetPath
from os import path

def str2sec(string):
    """字符串转秒数"""
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

def sec2str(seconds):
    """秒数转字符串"""
    m, s = divmod(seconds, 60)
    if m == 0:
        return seconds
    h, m = divmod(m, 60)
    if h == 0:
        string = "%02d:%02d" % (m, s)
    else:
        string = "%02d:%02d:%02d" % (h, m, s)
    return string

def add_txt_to_img_center(filename:str, text:str, fontpath:str, color):
    """在图片中央添加文字"""
    # 导入图片（解决中文路径乱码问题）
    img_path = path.join(GetPath(), filename)
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    # 读取图片，并手动将 BGR(A) 调整为 RGB(A)
    if filename[-3:] == "png":
        b_channel, g_channel, r_channel, a_channel = cv2.split(img)
        img_RGBA = cv2.merge((r_channel, g_channel, b_channel, a_channel))
        img_pil = Image.fromarray(img_RGBA)
    else:
        b_channel, g_channel, r_channel = cv2.split(img)
        img_RGB = cv2.merge((r_channel, g_channel, b_channel))
        img_pil = Image.fromarray(img_RGB)
    # 确定合适的字号
    width, height = img_pil.size
    fontsize = min(int(0.8 * width / len(text)), int(0.8 * height))
    font = ImageFont.truetype(fontpath, fontsize)
    # 精确处理文字位置（居中）
    x_0, y_0, x_1, y_1 = font.getbbox(text)    # 获取边界框，处理可能的 offset
    position = ((width - x_1 - x_0) / 2, (height - y_1 - y_0) / 2)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=color)
    img = np.array(img_pil)
    return img
