#! /usr/bin/python
# -*- coding: utf-8 -*-


class physics:

    def __init__(self, animation):

        self.move = []
        self.turn = []
        self.gunTurn = []
        self.radarTurn = []
        self.fire = []
        self.currentList = []
        self.animation = animation

        self.step = 5

    def reverse(self):
        """
        反转当前动画列表的播放顺序，实现动画的反向播放。

        参数：
            无

        返回值：
            无
        """
        self.animation.list.reverse()

    def newAnimation(self):
        """
        创建新的动画并添加到动画列表中。

        参数：
            无

        返回值：
            无
        """
        currentList = self.makeAnimation()
        if currentList != []:
            self.animation.list.append(currentList)
            self.clearAnimation()

    def makeAnimation(self, a=None):
        """
        根据保存的移动、转向、炮塔转向、雷达转向和开火动作，生成一个新的动画列表。

        参数：
            a (可选): 额外的参数，默认为 None

        返回值：
            list: 包含所有动画帧的字典列表
        """
        for i in range(
            max(
                len(self.move),
                len(self.turn),
                len(self.gunTurn),
                len(self.radarTurn),
                len(self.fire),
            )
        ):
            try:
                m = self.move[i]
            except IndexError:
                m = 0
            try:
                t = self.turn[i]
            except IndexError:
                t = 0
            try:
                g = self.gunTurn[i]
            except IndexError:
                g = 0
            try:
                r = self.radarTurn[i]
            except IndexError:
                r = 0
            try:
                f = self.fire[i]
            except IndexError:
                f = 0
            self.currentList.append(
                {"move": m, "turn": t, "gunTurn": g, "radarTurn": r, "fire": f}
            )
        self.currentList.reverse()
        return self.currentList

    def clearAnimation(self):
        """
        清空所有动画列表，包括移动、转向、炮塔转向、雷达转向、开火动作和当前列表。

        参数：
            无

        返回值：
            无
        """
        self.move = []
        self.turn = []
        self.gunTurn = []
        self.radarTurn = []
        self.fire = []
        self.currentList = []

    def reset(self):
        """
        重置动画的所有状态，包括清空动画列表和重置动画列表。

        参数：
            无

        返回值：
            无
        """
        self.clearAnimation()
        self.animation.list = []
