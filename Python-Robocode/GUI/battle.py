# -*- coding: utf-8 -*-

"""
Module implementing Battle.
"""

import os
import pickle
from loguru import logger

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from robot import Robot
from Ui_battle import Ui_Dialog


class Battle(QDialog, Ui_Dialog):
    """
    类文档在这里
    """

    def __init__(self, parent=None):
        """
        初始化 MainWindow 类的实例

        这个构造函数的主要作用是初始化窗口，设置界面，加载可用的机器人文件，并在列表框中展示机器人的名称

        参数：
            parent（QWidget，可选）：此窗口的父窗口。默认情况下，它是没有父窗口的

        返回值：
            无

        使用示例：
            在创建 MainWindow 的实例时，通常不需要传递 parent 参数，例如：
            main_window = MainWindow()

        异常处理：
            在导入机器人模块的过程中，如果发生任何异常，它将被捕获并打印到控制台，但不会终止程序执行
        """
        # 初始化父类 QDialog，以确保继承父类的所有属性和方法
        QDialog.__init__(self, parent)

        # 调用自定义的 setupUi 方法，这个方法应该被定义在类的另一个部分，通常是通过 Qt Designer 自动生成的
        self.setupUi(self)

        # 设置当前窗口的父窗口
        self.window = parent

        # 创建一个字典来存储机器人的名称和对应的类，用于后续创建机器人实例
        self.listBots = {}
        self.load_robot_code()

        # 将字典中的所有键（机器人名称）添加到列表框中
        for key in self.listBots.keys():
            self.listWidget.addItem(key)

    def load_robot_code(self):
        # 创建一个空列表来存储机器人的名称
        botnames = []
        # 获取当前目录下 Robots 文件夹中的所有文件
        botFiles = os.listdir(os.getcwd() + "/Robots")

        # 遍历所有文件，查找以.py 结尾的文件，这些文件代表着机器人模块
        for botFile in botFiles:
            if botFile.endswith(".py"):
                # 获取机器人文件的名称，并去掉.py 后缀
                botName = botPath = botFile[: botFile.rfind(".")]

                # 如果机器人名称不在列表中，添加到列表中
                if botName not in botnames:
                    botnames.append(botName)

                    try:
                        """
                        在指定的目录下搜索机器人模块文件（.py 文件）并导入它们。
                        它遍历这些模块，寻找继承自Robot类的子类。
                        如果找到这样的子类，它将创建该子类的一个实例，将实例添加到名为self.listBots的字典中，
                        并终止对模块属性的内部循环，因为已经找到了一个机器人子类。
                        """
                        # 导入机器人模块
                        logger.info(f"botPath:{botPath}")
                        botModule = __import__(botPath)

                        # 遍历模块中的所有属性
                        for name in dir(botModule):
                            # 判断属性值是否为机器人的子类
                            if getattr(botModule, name) in Robot.__subclasses__():
                                # 将第一个找到的机器人子类赋值给变量 someBot
                                someBot = getattr(botModule, name)
                                # 创建机器人实例并赋值给变量 bot
                                bot = someBot
                                # 将机器人实例添加到字典中，键为机器人的名称，值为机器人实例
                                self.listBots[
                                    str(bot).replace("<class '", "").replace("'>", "")
                                ] = bot
                                # 终止内部循环，因为已经找到了一个机器人子类
                                break
                    except Exception as e:
                        # 打印导入机器人模块过程中发生的异常信息
                        print("Problem with bot file '{}': {}".format(botFile, str(e)))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        点击添加机器人按钮时的槽函数
        """
        self.listWidget_2.addItem(self.listWidget.currentItem().text())

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        点击删除机器人按钮时的槽函数
        """
        item = self.listWidget_2.takeItem(self.listWidget_2.currentRow())
        if item is not None:
            del item

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        选择好机器人列表后的start按钮
        点击开始按钮时的槽函数
        """
        width = self.spinBox.value()
        height = self.spinBox_2.value()
        botList = []
        for i in range(self.listWidget_2.count()):

            key = str(self.listWidget_2.item(i).text())
            botList.append(self.listBots[key])

        self.save(width, height, botList)
        self.window.setUpBattle(width, height, botList)

    def save(self, width, height, botList):
        """
        保存战斗信息到文件

        参数:
            width (int): 战斗区域的宽度
            height (int): 战斗区域的高度
            botList (list): 机器人列表

        返回:
            None
        """
        dico = {}
        dico["width"] = width
        dico["height"] = height
        dico["botList"] = botList
        if self.debug.isChecked():
            dico["debug"] = True
        else:
            dico["debug"] = False

        if not os.path.exists(os.getcwd() + "/.datas/"):
            os.makedirs(os.getcwd() + "/.datas/")

        with open(os.getcwd() + "/.datas/lastArena", "wb") as file:
            pickler = pickle.Pickler(file)
            pickler.dump(dico)
        file.close()
