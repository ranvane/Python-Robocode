#! /usr/bin/python
# -*- coding: utf-8 -*-


# 定义animation类，用于播放动画效果
class animation:

    def __init__(self, name):
        """
        初始化animation对象

        参数：
            name（str）：动画的名称
        """
        self.list = []
        self.name = name
