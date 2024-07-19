#! /usr/bin/python
# -*- coding: utf-8 -*-

# 导入 sys 模块，用于访问 Python 解释器相关的特性
import sys
# 导入 os 模块，用于处理操作系统相关的任务，如文件路径等
import os

# 将当前工作目录下的 "GUI" 子目录添加到 Python 模块搜索路径中
sys.path.append(os.getcwd() + "/GUI")
# 将当前工作目录下的 "Objects" 子目录添加到 Python 模块搜索路径中
sys.path.append(os.getcwd() + "/Objects")
# 将当前工作目录下的 "robotImages" 子目录添加到 Python 模块搜索路径中
sys.path.append(os.getcwd() + "/robotImages")
# 将当前工作目录下的 "Robots" 子目录添加到 Python 模块搜索路径中
sys.path.append(os.getcwd() + "/Robots")
# 从 "window" 模块中导入 "MainWindow" 类，该类用于创建主窗口
from window import MainWindow
# 从 PyQt5.QtWidgets 模块中导入 QApplication 类，这是 PyQt5 应用程序的基础
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    '''
    启动应用程序的主循环，并通过 sys.exit() 确保程序在退出前清理资源
    
    '''
    # 创建 QApplication 对象，这是每个 PyQt5 应用程序的核心
    app = QApplication(sys.argv)
    # 设置应用程序的名称
    app.setApplicationName("Python-Robocode")
    # 创建 MainWindow 对象，这将是我们的应用程序的主要窗口
    myapp = MainWindow()
    # 显示 MainWindow 对象
    myapp.show()
    # 启动应用程序的主循环，并通过 sys.exit() 确保程序在退出前清理资源
    sys.exit(app.exec_())
