#! /usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsPolygonItem,
    QGraphicsEllipseItem,
)
from PyQt5.QtGui import QPolygonF, QColor, QBrush, QPen


class radarField(QGraphicsItemGroup):
    """
    根据传入的参数类型（poly或round）来创建不同形状的雷达区域
    """

    def __init__(self, qPointList, bot, rType):
        """
        初始化radarField对象

        参数：
            qPointList：点列表，可以是多边形的顶点列表，或圆形的矩形参数列表（x, y, width, height）
            bot：与雷达区域关联的机器人对象
            rType：区域类型，可以是"poly"（多边形）或"round"（圆形）
        """
        # 调用父类QGraphicsItemGroup初始化
        QGraphicsItemGroup.__init__(self)
        # 设置区域类型
        self.rType = rType

        # 根据rType创建相应的图形项
        if rType == "poly":
            # 创建多边形项
            self.item = QGraphicsPolygonItem()
            # 设置多边形顶点
            self.polygon = QPolygonF(qPointList)
            # 将多边形设置到项中
            self.item.setPolygon(self.polygon)
        elif rType == "round":
            # 创建圆形项（使用QGraphicsEllipseItem）
            self.item = QGraphicsEllipseItem()
            # 设置圆形项的边界矩形
            self.item.setRect(
                qPointList[0], qPointList[1], qPointList[2], qPointList[3]
            )

        # 设置关联的机器人对象
        self.robot = bot

        # 设置颜色、笔刷和画笔
        color = QColor(255, 100, 6, 10)
        brush = QBrush(color)
        pen = QPen(color)
        self.item.setBrush(brush)
        self.item.setPen(pen)

        # 将项添加到组中
        self.addToGroup(self.item)

    def setVisible(self, bol):
        """
        根据传入的布尔值设置雷达区域的可见性

        参数：
            bol：布尔值，True表示可见，False表示不可见
        """
        if bol:
            color = QColor(255, 100, 6, 15)  # 设置可见时的颜色
        else:
            color = QColor(255, 100, 6, 0)  # 设置不可见时的颜色
        brush = QBrush(color)
        pen = QPen(color)
        self.item.setBrush(brush)
        self.item.setPen(pen)
