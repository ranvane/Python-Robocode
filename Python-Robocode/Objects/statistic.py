#! /usr/bin/python
# -*- coding: utf-8 -*-


class statistic:

    def __init__(self):
        """
        初始化对象，设置统计信息的初始值

        这个方法用于初始化对象，设置.first、.second、.third和.points属性的默认值。

        它们分别代表第一名的次数、第二名的次数、第三名的次数和总积分。

        参数：
            无

        返回值：
            无
        """
        self.first = 0
        self.second = 0
        self.third = 0
        self.points = 0
