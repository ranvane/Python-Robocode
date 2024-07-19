#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import math

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QColor, QPainter


class Bullet(QGraphicsPixmapItem):
    """
    用于创建和管理游戏中的子弹对象
    """

    def __init__(self, power, color, bot):
        """
        初始化子弹对象

        参数：
            power（float）：子弹的威力，影响子弹的大小
            color（QColor）：子弹的颜色
            bot（object）：拥有此子弹的机器人对象
        """
        # 调用父类QGraphicsPixmapItem初始化
        QGraphicsPixmapItem.__init__(self)
        # graphics
        self.maskColor = QColor(255, 128, 0)
        self.pixmap = QPixmap(os.getcwd() + "/robotImages/blast.png")
        self.setPixmap(self.pixmap)
        self.setColour(color)
        self.isfired = False
        # physics
        self.width = self.boundingRect().width()
        self.height = self.boundingRect().height()
        if power <= 0.5:
            power = 0.5
        elif power >= 10:
            power = 10
        self.power = power
        bsize = power
        if power < 3:
            bsize = 4
        self.pixmap = self.pixmap.scaled(bsize, bsize)
        self.setPixmap(self.pixmap)
        self.robot = bot

    def init(self, pos, angle, scene):
        """
        初始化子弹的位置、角度和所属场景

        参数：
            pos（QPointF）：子弹的初始位置
            angle（float）：子弹的发射角度
            scene（QGraphicsScene）：子弹所属的场景
        """
        self.angle = angle
        self.setPos(pos)
        self.scene = scene
        self.isfired = True

    def setColour(self, color):
        """
        设置子弹的颜色

        参数：
            color（QColor）：新的颜色
        """
        mask = self.pixmap.createMaskFromColor(self.maskColor, 1)
        p = QPainter(self.pixmap)
        p.setPen(color)
        p.drawPixmap(self.pixmap.rect(), mask, mask.rect())
        p.end()
        self.setPixmap(self.pixmap)
        self.maskColor = color

    def advance(self, i):
        """
        每一帧的动画更新

        参数：
            i（int）：动画的当前帧数
        """
        if self.isfired:

            pos = self.pos()
            x = pos.x()
            y = pos.y()
            dx = -math.sin(math.radians(self.angle)) * 10.0
            dy = math.cos(math.radians(self.angle)) * 10.0
            self.setPos(x + dx, y + dy)
            if x < 0 or y < 0 or x > self.scene.width or y > self.scene.height:
                self.robot.onBulletMiss(id(self))
                self.scene.removeItem(self)
                self.robot.removeMyProtectedItem(self)
