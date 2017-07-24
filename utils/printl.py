# -*- coding:utf-8 -*-

# 概述：打印到日志（必选）和控制台（可选）

import os
import re

def printl(logline, logfilePath, toConsole=True, reset=False):

    logfileName = re.sub(r'.*\\.+\\', '', logfilePath)  # 获得文件名

    logfileDir = re.sub(r'[^\\]*$', '', logfilePath)  # 获得文件所在目录

    if not os.path.isdir(logfileDir):  # 该目录不存在就创建
        os.makedirs(logfileDir)

    if reset:  # 如果复位就从头开始写
        with open(logfilePath, "w") as f:
            print >> f,logline

    else:  # 否则就接着写
        with open(logfilePath, "a") as f:
            print >> f,logline
            
    if toConsole:  # 如果要顺便打印到控制台
        print(logline)  # 就打印到控制台