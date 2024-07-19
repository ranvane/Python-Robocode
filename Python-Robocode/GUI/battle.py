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
    类 Battle，继承自 QDialog 和 Ui_Dialog 类。这是一个使用 PyQt5 库创建的图形界面应用程序的主窗口。

    以下是该类的一些主要方法和属性：

    __init__(self, parent=None): 
        构造函数，初始化 MainWindow 类的实例。它首先调用父类 QDialog 的构造函数，确保继承了所有父类的属性和方法。然后它调用了 setupUi 方法，这个方法应该是在 Ui_Dialog 类中定义的，用于初始化界面。接着，它创建了一个字典 listBots 来存储机器人的信息，这个字典的键是机器人的名称，值是机器人的实例。然后它调用 load_robot_code 方法加载机器人代码。最后，它将字典中的所有机器人名称添加到列表框中，以便用户可以选择它们。

    load_robot_code(self):
        这个方法的目的是自动化加载位于当前目录下的 Robots 文件夹中的所有机器人模块。它首先创建一个空列表 botnames 来存储已加载的机器人的名字。然后获取 Robots 文件夹中的所有文件名，并遍历这个列表。对于每个文件名，如果它是以.py 结尾的，我们去掉.py 后缀，得到机器人的名字 botName。如果 botName 不在 botnames 列表中，它将被添加到列表中。然后我们尝试导入这个机器人模块。如果导入成功，我们遍历模块中的所有属性。如果属性是 Robot 类的子类，我们创建这个子类的实例，并将实例存储在 listBots 字典中。同时，它将终止内部循环，因为已经找到了一个机器人子类。如果在这个过程中发生任何异常，它将被打印到控制台，但程序不会终止，而是会继续加载其他机器人模块。

    on_pushButton_clicked(self):
        这个槽函数与界面上的添加机器人按钮相关联。当点击这个按钮时，它将获取当前在列表框中选中的机器人名称，并将其添加到另一个列表框 listWidget_2 中。

    on_pushButton_2_clicked(self):
        这个槽函数与界面上的删除机器人按钮相关联。当点击这个按钮时，它将删除在列表框 listWidget_2 中当前选中的机器人条目。如果条目被成功删除，它将被打印到控制台。

    on_pushButton_3_clicked(self):
        这个槽函数与界面上的 start 按钮相关联。当点击这个按钮时，它将获取 spinBox 和 spinBox_2 中的值，分别作为战斗区域的宽度和高度。然后它将创建一个名为 botList 的列表，并遍历 listWidget_2 中的每个条目。对于每个条目，它将获取其文本值，并从 listBots 字典中获取相应的机器人实例。这些实例将被添加到 botList 列表中。最后，它调用 save 方法保存战斗信息，并调用 setUpBattle 方法设置战斗。

    save(self, width, height, botList):
        这个方法负责保存战斗信息到文件。它创建一个字典 dico，其中包含战斗区域的宽度、高度、机器人列表以及一个表示是否调试的布尔值。然后它创建一个名为.datas 的目录（如果它不存在）。最后，它打开一个名为 lastArena 的文件，使用 pickle 将 dico 字典保存到文件中，并关闭文件。

    这个类使用了一些 Python 模块，如 os、pickle 和 loguru，以及自定义的 robot 和 Ui_battle 模块。同时，它使用了 PyQt5 的 QDialog、QWidget、QSpinBox 和 QListWidget 类来创建和操作图形界面。
    """
    def __init__(self, parent=None):
        """
        初始化 Battle 类的实例

        参数：
            parent（QWidget，可选）：此窗口的父窗口。默认情况下，它是没有父窗口的

        返回值：
            无

        使用示例：
            在创建 Battle 的实例时，通常不需要传递 parent 参数，例如：
            battle = Battle()

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
        """
        这个函数的目的是加载并初始化所有位于当前目录下的Robots文件夹中的机器人模块。以下是该函数的主要功能和步骤：

        这个函数的设计旨在自动化机器人模块的加载过程，使其易于扩展和维护。

        返回:
            None

        异常处理:
            在加载机器人模块过程中，如果发生任何异常，将会把异常信息进行输出，但是程序不会终止，而是会继续加载其他的机器人模块。
        """
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
                        # 尝试导入机器人模块
                        logger.info(f"botPath:{botPath}")
                        botModule = __import__(botPath)

                        # 遍历模块中的所有属性
                        for name in dir(botModule):
                            # 对于模块中的每个属性，使用getattr函数获取属性的值，并检查它是否是Robot类的子类。
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
