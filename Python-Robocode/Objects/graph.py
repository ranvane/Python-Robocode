#! /usr/bin/python
# -*- coding: utf-8 -*-

# 导入所需的模块和类
import time, os, random
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QColor, QBrush
from PyQt5.QtCore import QPointF, QRectF
from robot import Robot
from outPrint import outPrint
from loguru import logger


# 创建图形场景类Graph，继承自QGraphicsScene
class Graph(QGraphicsScene):

    # 初始化函数
    def __init__(self, parent, width, height):
        # 调用父类QGraphicsScene的初始化函数
        QGraphicsScene.__init__(self, parent)
        # 设置场景的大小为width和height
        self.setSceneRect(0, 0, width, height)
        # 获取场景的父窗口对象self.Parent
        self.Parent = parent

        # self.Parent.graphicsView.centerOn(250, 250)
        # 保存场景的宽度和高度
        self.width = width
        self.height = height
        # 获取场景中的网格点列表
        self.grid = self.getGrid()
        # 设置场景的背景和墙壁纹理
        self.setTiles()

    # 获取场景中的网格点列表
    def getGrid(self):
        # 根据场景宽度和高度计算网格的行和列
        w = int(self.width / 80)
        h = int(self.height / 80)
        # 创建一个空列表用于存储网格点
        l = []
        # 遍历行和列生成网格点的坐标
        for i in range(w):
            for j in range(h):
                # 将网格点坐标添加到列表中
                l.append(QPointF((i + 0.5) * 80, (j + 0.5) * 80))
        return l

    # 设置场景的背景和墙壁纹理
    def setTiles(self):
        # 设置背景颜色
        # 背景
        brush = QBrush()
        # 设置背景图片
        pix = QPixmap(os.getcwd() + "/robotImages/tile.png")
        # 将图片设置为纹理
        brush.setTexture(pix)
        # 设置图片重复方式
        brush.setStyle(24)
        # 设置场景背景
        self.setBackgroundBrush(brush)

        # 设置墙壁纹理
        # 墙壁
        # 左边墙壁
        left = QGraphicsRectItem()
        # 设置墙壁图片
        pix = QPixmap(os.getcwd() + "/robotImages/tileVert.png")
        # 设置墙壁大小
        left.setRect(QRectF(0, 0, pix.width(), self.height))
        # 设置墙壁纹理
        brush.setTexture(pix)
        # 设置图片重复方式
        brush.setStyle(24)
        # 设置墙壁颜色
        left.setBrush(brush)
        # 给墙壁命名
        left.name = "left"
        # 添加墙壁到场景
        self.addItem(left)
        # 右边墙壁
        right = QGraphicsRectItem()
        # 设置墙壁大小
        right.setRect(self.width - pix.width(), 0, pix.width(), self.height)
        # 设置墙壁颜色
        right.setBrush(brush)
        # 命名为right
        right.name = "right"
        # 添加right到场景
        self.addItem(right)
        # 顶部墙壁
        top = QGraphicsRectItem()
        # 设置图片
        pix = QPixmap(os.getcwd() + "/robotImages/tileHori.png")
        # 设置大小
        top.setRect(QRectF(0, 0, self.width, pix.height()))
        # 设置颜色
        brush.setTexture(pix)
        # 设置Style
        brush.setStyle(24)
        # 设置颜色
        top.setBrush(brush)
        # 命名
        top.name = "top"
        # 添加物品到场景
        self.addItem(top)
        # 底部墙壁
        bottom = QGraphicsRectItem()
        # 设置大小
        bottom.setRect(0, self.height - pix.height(), self.width, pix.height())
        # 设置颜色
        bottom.setBrush(brush)
        # 命名
        bottom.name = "bottom"
        # 添加物品到场景
        self.addItem(bottom)

    # 在场景中添加机器人
    def AddRobots(self, botList):
        """ """
        # 创建一个空列表用于存储活着的机器人对象
        self.aliveBots = []
        # 创建一个空列表用于存储死亡的机器人对象
        self.deadBots = []
        try:
            # 从grid列表中随机获取机器人的初始位置点
            posList = random.sample(self.grid, len(botList))
            for bot in botList:
                try:
                    # 创建一个机器人对象，并将其添加到图形场景中
                    robot = bot(self.sceneRect().size(), self, str(bot))
                    self.aliveBots.append(robot)
                    self.addItem(robot)
                    # 将机器人放置在场景中的随机位置
                    robot.setPos(posList.pop())
                    # 将机器人信息添加到父窗口对象中
                    self.Parent.addRobotInfo(robot)
                except Exception as e:
                    # 打印机器人文件发生错误时的警告信息
                    print("Problem with bot file '{}': {}".format(bot, str(e)))

            # 关闭父窗口的战斗菜单
            self.Parent.battleMenu.close()
        except ValueError:
            # 弹出警告框，提示地图尺寸太小，无法容纳所有机器人
            QMessageBox.about(self.Parent, "Alert", "Too many Bots for the map's size!")
        except AttributeError:
            # 忽略属性错误
            pass

    def battleFinished(self):
        # 打印战斗结束信息
        print("battle terminated")
        try:
            # 将活着的机器人对象添加到死亡机器人列表中
            self.deadBots.append(self.aliveBots[0])
            # 从图形场景中移除活着的机器人对象
            self.removeItem(self.aliveBots[0])
        except IndexError:
            # 如果活着的机器人列表为空，忽略移除操作
            pass
        # 获取死亡机器人列表的长度
        j = len(self.deadBots)

        # 遍历死亡机器人列表
        for i in range(j):
            # 打印死亡机器人的信息和排名（根据死亡顺序）
            print("N° {}:{}".format(j - i, self.deadBots[i]))
            # 根据死亡排名更新统计信息
            if j - i == 1:  # first place
                self.Parent.statisticDico[repr(self.deadBots[i])].first += 1
            if j - i == 2:  # 2nd place
                self.Parent.statisticDico[repr(self.deadBots[i])].second += 1
            if j - i == 3:  # 3rd place
                self.Parent.statisticDico[repr(self.deadBots[i])].third += 1

            # 更新死亡机器人的积分
            self.Parent.statisticDico[repr(self.deadBots[i])].points += i

        # 战斗结束后，让父窗口对象选择下一步操作
        self.Parent.chooseAction()

    def setTiles(self):
        """
        设置游戏场景的背景和墙壁纹理

        参数：
            无

        返回值：
            无
        """
        # 设置背景
        brush = QBrush()
        pix = QPixmap(os.getcwd() + "/robotImages/tile.png")
        brush.setTexture(pix)
        brush.setStyle(24)
        self.setBackgroundBrush(brush)

        # 设置墙壁
        # 左边墙壁
        left = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileVert.png")
        left.setRect(QRectF(0, 0, pix.width(), self.height))
        brush.setTexture(pix)
        brush.setStyle(24)
        left.setBrush(brush)
        left.name = "left"
        self.addItem(left)
        # 右边墙壁
        right = QGraphicsRectItem()
        right.setRect(self.width - pix.width(), 0, pix.width(), self.height)
        right.setBrush(brush)
        right.name = "right"
        self.addItem(right)
        # 顶部墙壁
        top = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileHori.png")
        top.setRect(QRectF(0, 0, self.width, pix.height()))
        brush.setTexture(pix)
        brush.setStyle(24)
        top.setBrush(brush)
        top.name = "top"
        self.addItem(top)
        # 底部墙壁
        bottom = QGraphicsRectItem()
        pix = QPixmap(os.getcwd() + "/robotImages/tileHori.png")
        bottom.setRect(0, self.height - pix.height(), self.width, pix.height())
        brush.setTexture(pix)
        brush.setStyle(24)
        bottom.setBrush(brush)
        bottom.name = "bottom"
        self.addItem(bottom)


def getGrid(self):
    """
    获取场景中的网格点列表

    返回值：
        list：包含场景中所有网格点的QPointF对象列表

    使用示例：
        >>> grid_list = getGrid()
    """
    # 根据场景宽度和高度计算网格的行和列
    w = int(self.width / 80)
    h = int(self.height / 80)

    # 创建一个空列表用于存储网格点
    l = []

    # 遍历行和列生成网格点的坐标
    for i in range(w):
        for j in range(h):
            # 将网格点坐标添加到列表中
            l.append(QPointF((i + 0.5) * 80, (j + 0.5) * 80))

    return l
