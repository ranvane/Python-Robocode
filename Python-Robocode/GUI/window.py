# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import os, pickle

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, QTimer

from graph import Graph
from Ui_window import Ui_MainWindow
from battle import Battle
from robot import Robot
from RobotInfo import RobotInfo
from statistic import statistic
from loguru import logger


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    码构建了一个功能丰富的机器人战斗模拟程序，用户可以通过界面与程序交互，加载机器人代码，
    开始或复用上次的战斗，控制战斗节奏，查看统计信息等。
    """

    def __init__(self, parent=None):
        """
        这是一个初始化方法，在创建类的实例时被调用，用于设置窗口的初始状态和属性。

        参数：
            parent（QWidget，可选）：该窗口的父窗口。默认为None，表示没有父窗口。

        返回：
            无

        使用示例：
            my_window = MyWindow()  # 创建了一个名为my_window的MyWindow实例
        """
        # 调用父类QMainWindow的__init__方法，确保继承了QMainWindow的所有属性和方法
        QMainWindow.__init__(self, parent)

        # 调用自定义设置窗口界面的方法setupUi(self)，该方法通常位于类的最下方，由Qt Designer自动生成
        self.setupUi(self)

        # 初始化变量countBattle，可能是用于记录战斗次数，初始值为0
        self.countBattle = 0

        # 创建一个QTimer对象，用于以后的时间控制任务，例如动画，更新进度条等
        self.timer = QTimer()

        # 将QTableWidget的水平表头（列标题）设置为根据内容自动调整大小的模式，这使得表格更加整洁和易于阅读
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 隐藏tableWidget，可能是为了在需要时才显示，减少界面的复杂性
        self.tableWidget.hide()

        # 初始化统计数据字典，用于存储机器人的统计信息
        self.statisticDico = {}
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
        响应按钮点击事件，加载并复用上次战斗信息
        Strat Last Battle 按钮的点击事件处理函数

        当用户点击触发此方法的按钮时，程序会检查当前目录下是否存在名为`.datas/lastArena`的文件。如果文件存在，它将读取文件内容，反序列化后加载到字典`dico`中，并提取出宽、高和机器人数组等信息，用于初始化新的战斗设置。如果文件不存在，程序将打印一条消息提示用户没有找到上次的竞技场信息。

        参数：
            无

        返回：
            无

        使用示例：
            这段代码通常被放在一个类中，用户点击按钮后，会调用此方法。方法内的逻辑会复用之前的战斗信息来初始化新的战斗。
        """

        print("Strat Last Battle...")

        if os.path.exists(os.getcwd() + "/.datas/lastArena"):
            with open(os.getcwd() + "/.datas/lastArena", "rb") as file:
                unpickler = pickle.Unpickler(file)
                dico = unpickler.load()
            file.close()
        else:
            print("No last arena found.")

        if dico["debug"]:
            self.setUpBattle(dico["width"], dico["height"], dico["botList"])
        else:
            self.setUpBattle(dico["width"], dico["height"], dico["botList"])

    def setUpBattle(self, width, height, botList):
        """
        初始化战斗场景，设置场景大小，显示战斗画面，创建参战机器人统计信息字典，并启动战斗。

        参数：
            width（int）：战斗区域的宽度。
            height（int）：战斗区域的高度。
            botList（list）：参战的机器人列表，每个元素都是一个机器人对象。

        返回：
            无

        使用示例：
            setUpBattle(800, 600, [bot1, bot2, bot3])
        """
        # 清空表格的内容，可能是移除之前的战斗数据或其他信息
        self.tableWidget.clearContents()

        # 隐藏表格，这表明在当前的战斗设置中，表格（可能是显示信息的表格）不被需要或不应该被显示
        self.tableWidget.hide()

        # 显示图形视图，这可能是用于显示战斗场景的窗口，用户将通过这个视图观看战斗过程
        self.graphicsView.show()

        # 设置战斗场景的宽度，这将决定场景中元素的布局和显示方式
        self.width = width

        # 设置战斗场景的高度，这将决定场景中元素的布局和显示方式
        self.height = height

        # 存储参战的机器人列表，这使得在后续的战斗逻辑中，可以通过列表访问每个机器人对象
        self.botList = botList

        # 创建一个空字典，用于存储每个机器人的统计信息，字典的键是机器人的名称或标识符，值是包含统计数据的对象
        self.statisticDico = {}

        # 遍历参战的机器人列表
        for bot in botList:
            # 对于列表中的每个机器人，使用它的名称或标识符作为键，创建一个新的统计对象，并将其添加到字典中
            self.statisticDico[self.repres(bot)] = statistic()

        # 启动战斗，这个方法可能会初始化一些战斗所需的其他组件，比如计时器（QTimer），用来控制战斗的节奏
        self.startBattle()

    def startBattle(self):
        """
        启动战斗流程
        这个方法负责启动战斗流程，它执行以下操作：
            1. 断开并删除旧的计时器，以及旧的场景和菜单场景，确保它们不会干扰新的战斗。
            2. 创建一个新的计时器，重置战斗计数，并用于控制战斗的节奏。
            3. 创建新的图形场景，分别用于菜单和战斗场景。
            4. 将战斗场景设置为主图形视图的场景。
            5. 调用场景的 AddRobots 方法，添加机器人到战斗场景中。
            6. 连接计时器的 timeout 信号到场景的 advance 方法，使得每次计时器超时时，场景能够前进到下一帧。
            7. 根据水平滑块的值计算一个新的时间间隔，并设置为计时器的启动间隔。
            8. 调用 resizeEvent 方法，确保战斗场景在窗口大小调整时能够正确显示。
        返回值：
            无
        参数：
            无
        使用示例：
            调用这个方法即可开始新的战斗流程。
        """
        try:
            self.timer.timeout.disconnect(self.scene.advance)
            del self.timer
            del self.scene
            del self.sceneMenu
        except:
            pass

        self.timer = QTimer()
        self.countBattle += 1
        self.sceneMenu = QGraphicsScene()
        self.graphicsView_2.setScene(self.sceneMenu)
        self.scene = Graph(self, self.width, self.height)

        self.graphicsView.setScene(self.scene)
        self.scene.AddRobots(self.botList)
        self.timer.timeout.connect(self.scene.advance)
        tmp = (self.horizontalSlider.value() ** 2) / 100.0
        self.timer.start(int(tmp))
        self.resizeEvent()

    @pyqtSlot(int)
    def on_horizontalSlider_valueChanged(self, value):
        """
        当水平滑块的值发生变化时，这个方法会被调用。

        参数：
            value（int）：滑块的当前值。

        返回值：
            None

        使用示例：
            这个方法是一个事件处理程序，当用户移动水平滑块时，它会自动被调用。方法内部会根据滑块的当前值调整计时器（self.timer）的间隔。具体来说，它会按照滑块值的平方除以 100.0 来计算新的计时器间隔，并使用setInterval方法设置这个间隔。这样，随着用户调整滑块，计时器的更新频率会相应地改变。
        """
        self.timer.setInterval((value**2) / 100.0)

    @pyqtSlot()
    def on_actionNew_triggered(self):
        """

        显示 新建 菜单

        参数:
            无

        返回:
            无

        使用示例:
            当用户选择新建时，将创建一个 Battle 实例并显示它
        """
        self.battleMenu = Battle(self)
        self.battleMenu.show()

    @pyqtSlot()
    def on_actionNew_2_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print("Not Implemented Yet")

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        print("Not Implemented Yet")

    def resizeEvent(self, evt=None):
        """
        处理窗口大小调整事件

        当窗口大小改变时，这个方法会被自动调用。它的主要目的是调整图形视图（QGraphicsView）的显示范围，以便在窗口尺寸变化时始终能够看到整个场景（QGraphicsScene）。fitInView() 函数会根据传入的矩形参数自动调整视图的大小，在这个例子中的矩形参数设置为场景的边界矩形（self.scene.sceneRect()），这意味着视图将会缩放以使得整个场景都能被显示在视图窗口内。第二个参数 Qt.KeepAspectRatio 表示保持宽高比例，这样可以确保场景中的图形不会被拉伸或变形。

        参数：
            evt（QResizeEvent）：窗口大小变化事件的参数，表示窗口大小变化的相关信息

        返回：
            无

        使用示例：
            当用户调整窗口大小时，这个方法会自动被调用，无需手动调用

        异常处理：
            在 try 语句块中，我们尝试执行 fitInView 操作。如果操作失败（可能是由于场景或视图对象不存在），通过 except 语句块捕获异常并忽略它，确保程序不会因为错误而终止。
        """
        try:
            self.graphicsView.fitInView(self.scene.sceneRect(), 4)
        except:
            pass

    def addRobotInfo(self, robot):
        """
        这个函数的目的是为一个给定的机器人对象添加信息展示。

        参数：
            robot（对象）：机器人对象实例，包含机器人的相关信息。

        返回：
            无

        使用示例：
            addRobotInfo(robot_instance)
        """
        self.sceneMenu.setSceneRect(0, 0, 170, 800)
        # 为机器人创建一个信息展示面板
        rb = RobotInfo()
        # 设置按钮文本为机器人的名称或标识符
        rb.pushButton.setText(str(robot))
        # 设置进度条初始值为100%
        rb.progressBar.setValue(100)
        # 存储机器人对象的引用，以便后续操作
        rb.robot = robot
        # 建立机器人对象与信息展示面板的关联
        robot.info = rb
        robot.progressBar = rb.progressBar
        robot.icon = rb.toolButton
        robot.icon2 = rb.toolButton_2
        # 将信息展示面板添加到场景菜单中
        p = self.sceneMenu.addWidget(rb)
        # 获取当前场景中存活机器人的数量
        l = len(self.scene.aliveBots)
        # 根据存活机器人数量调整场景菜单的大小
        self.sceneMenu.setSceneRect(0, 0, 170, l * 80)
        # 设置新添加的机器人信息展示面板的位置
        p.setPos(0, (l - 1) * 80)

    def chooseAction(self):
        """
        根据条件判断是显示统计菜单还是开始新的战斗。
        如果当前战斗次数达到或超过旋转框中设定的值，则显示统计菜单并停止计时器；
        否则，开始新的战斗。

        参数：
            无

        返回：
            无

        使用示例：
            当用户达到一定数量的战斗后，显示统计信息，否则开始新的战斗
        """
        if self.countBattle >= self.spinBox.value():
            # 显示统计信息
            "Menu Statistic"
            self.graphicsView.hide()
            self.tableWidget.show()
            self.tableWidget.setRowCount(len(self.statisticDico))

            i = 0
            for key, value in self.statisticDico.items():
                self.tableWidget.setItem(i, 0, QTableWidgetItem(key))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(value.first)))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(value.second)))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(str(value.third)))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(str(value.points)))

                i += 1

            self.countBattle = 0
            self.timer.stop()
        else:
            self.startBattle()

    def repres(self, bot):
        repres = repr(bot).split(".")
        return repres[1].replace("'>", "")
