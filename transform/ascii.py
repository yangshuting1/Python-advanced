#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import argparse


# argparse:命令行解析包
parser = argparse.ArgumentParser()

# 增加add_argument()方法，在这个方法中，我们指定程序将要去接受的命令行选项，在这里我们命名为file(只是一个名字，可以随意更改)
# 此时，调用程序需要输入一个参数
# 方法parse_args()实际上会返回一些选项指定的值，上述例子中，file
# 在argparse模块中，当你指定位置参数名为echo时，此时想要提取该参数值，必须指定为args.file
parser.add_argument('file')  # 输入文件

parser.add_argument('-o', '--output')  # 输出文件

parser.add_argument('--width', type=int, default=60)  # 输出字符画 宽

parser.add_argument('--height', type=int, default=40)  # 输出字符画 高

# 获取参数

args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

# 字符画所使用的字符集，一共70个字符，字符的种类和数量可以自己根据字符画的效果反复调试
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# 将256灰度映射到70个字符上

def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '

    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)  # r:red / g:green/ b：blue

    unit = (256.0 + 1) / length

    return ascii_char[int(gray / unit)]


if __name__ == '__main__':
    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i)))
        txt += "\n"
    print txt

    # 字符输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open("output.txt", "w") as f:
            f.write(txt)
