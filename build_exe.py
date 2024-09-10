from setup_main import build_pyd
import os
import shutil
from glob import glob

"""
参考文档：https://zhuanlan.zhihu.com/p/162708225
1. 当前因为打包为 pyd 文件后，pyinstaller 工具无法分析文件的包依赖关系，
导致没有把一些系统dll和系统路径的包导入打包路径。这里需要把通过
--hidden-import 将系统包依赖包导入。
2. 需要手工将打包的 pyd 导入到打包以来目录下
"""

package_name = "build_pyd"


def copyFile(srcfile, dstpath):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.copy(srcfile, dstpath + fname)  # 复制文件


def run():
    # 打包 pyd 文件
    build_pyd()
    # 使用 --hidden-imort 导入系统和第三方包，打包 exe
    os.system(
        "pyinstaller build_pyd/server.py --hidden-import warnings --hidden-import random --hidden-import os --hidden-import datetime --hidden-import time --hidden-import re --hidden-import threading --hidden-import ctypes --hidden-import ctypes.wintypes --hidden-import comtypes --hidden-import comtypes.client --hidden-import PIL --hidden-import typing --hidden-import win32clipboard --hidden-import win32gui --hidden-import win32api --hidden-import win32con --hidden-import pyperclip --hidden-import psutil --hidden-import shutil --hidden-import winreg --hidden-import logging --hidden-import PIL.ImageGrab --hidden-import win32process --hidden-import comtypes.stream"
    )
    # 复制可能未引入的项目 pyd 文件，一直 pyinstaller 打包的pyd目标路径为 ./dist/server/_internal/libs
    src_root = "./" + package_name + "/libs/*"
    libs_files = glob(src_root)
    for srcfile in libs_files:
        if os.path.isdir(srcfile):
            continue
        copyFile(srcfile, "./dist/server/_internal/libs/")


if __name__ == "__main__":
    run()
