#! /usr/bin/python
# -*- coding: utf-8 -*-

# 导入time, os, math模块
import time, os, math

# 导入traceback模块，用于跟踪错误信息
import traceback

# 从PyQt5.QtWidgets模块导入QGraphicsItemGroup, QGraphicsPixmapItem, QGraphicsRectItem类
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsPixmapItem, QGraphicsRectItem

# 从PyQt5.QtGui模块导入QPixmap, QColor, QPainter, QIcon类
from PyQt5.QtGui import QPixmap, QColor, QPainter, QIcon

# 从PyQt5.QtCore模块导入QPointF类
from PyQt5.QtCore import QPointF

# 导入physics模块
from physics import physics

# 导入bullet模块
from bullet import Bullet

# 导入radarField模块
from radarField import radarField

# 导入animation模块
from animation import animation


# 定义Robot类，继承自QGraphicsItemGroup
class Robot(QGraphicsItemGroup):
    # 初始化Robot对象
    def __init__(self, mapSize, parent, repr):
        # 调用父类QGraphicsItemGroup的初始化方法
        QGraphicsItemGroup.__init__(self)
        # 初始化属性
        self.__mapSize = mapSize
        self.__parent = parent
        self.__health = 100
        self.__repr = repr
        self.__gunLock = "free"
        self.__radarLock = "Free"

        # 初始化动画
        self.__runAnimation = animation("run")
        self.__targetAnimation = animation("target")
        self.__physics = physics(self.__runAnimation)

        # 图形相关
        self.maskColor = QColor(0, 255, 255)
        self.gunMaskColor = QColor(0, 255, 255)
        self.radarMaskColor = QColor(0, 255, 255)

        # 加载图片
        # 创建QGraphicsPixmapItem对象表示机器人的基础部分
        self.__base = QGraphicsPixmapItem()
        # 设置基础部分的图片为当前工作目录下的baseGrey.png
        self.__base.pixmap = QPixmap(os.getcwd() + "/robotImages/baseGrey.png")
        # 设置图片到QGraphicsPixmapItem对象上
        self.__base.setPixmap(self.__base.pixmap)
        # 将QGraphicsPixmapItem对象添加到当前的Robot对象中，使其作为Robot对象的一个子项
        self.addToGroup(self.__base)
        # 获取基础部分图片的宽度
        self.__baseWidth = self.__base.boundingRect().width()
        # 获取基础部分图片的高度
        self.__baseHeight = self.__base.boundingRect().height()

        # 加载枪支图片
        self.__gun = QGraphicsPixmapItem()
        # 设置枪支图片为当前工作目录下的gunGrey.png
        self.__gun.pixmap = QPixmap(os.getcwd() + "/robotImages/gunGrey.png")
        # 设置图片到QGraphicsPixmapItem对象上
        self.__gun.setPixmap(self.__gun.pixmap)
        # 将QGraphicsPixmapItem对象添加到当前的Robot对象中，使其作为Robot对象的一个子项
        self.addToGroup(self.__gun)
        # 获取枪支图片的宽度
        self.__gunWidth = self.__gun.boundingRect().width()
        # 获取枪支图片的高度
        self.__gunHeight = self.__gun.boundingRect().height()
        # 枪支位置定位
        # 计算枪支在x轴的位置，使其位于基础部分的中心
        x = self.__base.boundingRect().center().x()
        # 计算枪支在y轴的位置，使其位于基础部分的中心
        y = self.__base.boundingRect().center().y()
        # 设置枪支的位置，使其位于基础部分的上方
        self.__gun.setPos(x - self.__gunWidth / 2.0, y - self.__gunHeight / 2.0)

        # 加载雷达图片
        self.__radar = QGraphicsPixmapItem()
        # 设置雷达图片为当前工作目录下的radar.png
        self.__radar.pixmap = QPixmap(os.getcwd() + "/robotImages/radar.png")
        # 设置图片到QGraphicsPixmapItem对象上
        self.__radar.setPixmap(self.__radar.pixmap)
        # 将QGraphicsPixmapItem对象添加到当前的Robot对象中，使其作为Robot对象的一个子项
        self.addToGroup(self.__radar)
        # 获取雷达图片的宽度
        self.__radarWidth = self.__radar.boundingRect().width()
        # 获取雷达图片的高度
        self.__radarHeight = self.__radar.boundingRect().height()
        # 雷达位置定位
        # 设置雷达的位置，使其位于基础部分的上方
        self.__radar.setPos(x - self.__radarWidth / 2.0, y - self.__radarHeight / 2.0)

        # 加载雷达领域（radarField）
        # 定义雷达领域的顶点坐标列表
        firstPoint = QPointF(x - self.__radarWidth / 2, y)
        secondPoint = QPointF(x + self.__radarWidth / 2, y)
        thirdPoint = QPointF(x + 4 * self.__radarWidth, y + 700)
        fourthPoint = QPointF(x - 4 * self.__radarWidth, y + 700)
        qPointListe = []
        # 将顶点坐标添加到列表中
        qPointListe.append(firstPoint)
        qPointListe.append(secondPoint)
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        # 创建雷达领域对象，参数包括顶点坐标列表、父对象和形状类型（这里是多边形poly）
        self.__radarField = radarField(qPointListe, self, "poly")

        # __largeRadarField
        # 从顶点坐标列表中移除第三个和第四个顶点，以创建一个新的领域对象
        qPointListe.remove(fourthPoint)
        qPointListe.remove(thirdPoint)
        # 定义新的第三个顶点坐标，相对于第二个顶点向右偏移
        thirdPoint = QPointF(x + 10 * self.__radarWidth, y + 400)
        # 定义新的第四个顶点坐标，相对于第一个顶点向左偏移
        fourthPoint = QPointF(x - 10 * self.__radarWidth, y + 400)
        # 将新的顶点坐标添加到列表中
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        # 使用更新后的顶点坐标列表创建一个新的雷达领域对象
        self.__largeRadarField = radarField(qPointListe, self, "poly")

        # thinRadarField
        # 再次从顶点坐标列表中移除第三个和第四个顶点
        qPointListe.remove(fourthPoint)
        qPointListe.remove(thirdPoint)
        # 定义新的第三个顶点坐标，相对于第二个顶点向右偏移
        thirdPoint = QPointF(x + 0.4 * self.__radarWidth, y + 900)
        # 定义新的第四个顶点坐标，相对于第一个顶点向左偏移
        fourthPoint = QPointF(x - 0.4 * self.__radarWidth, y + 900)
        # 将新的顶点坐标添加到列表中
        qPointListe.append(thirdPoint)
        qPointListe.append(fourthPoint)
        # 使用更新后的顶点坐标列表创建一个新的雷达领域对象
        self.__thinRadarField = radarField(qPointListe, self, "poly")

        # roundRadarField
        # 创建一个圆形雷达领域对象，参数包括圆心坐标列表、父对象和形状类型（这里是圆形round）
        self.__roundRadarField = radarField([0, 0, 300, 300], self, "round")
        # 将圆形雷达领域对象添加到当前的Robot对象中，使其作为Robot对象的一个子项
        self.addToGroup(self.__roundRadarField)
        # 设置圆形雷达领域对象的位置，使其位于基础部分的中心
        self.__roundRadarField.setPos(
            x - self.__roundRadarField.boundingRect().width() / 2.0,
            y - self.__roundRadarField.boundingRect().height() / 2.0,
        )

        # 将所有的雷达领域对象添加到当前的Robot对象中，使其作为Robot对象的子项
        self.addToGroup(self.__radarField)
        self.addToGroup(self.__largeRadarField)
        self.addToGroup(self.__thinRadarField)

        # 隐藏__largeRadarField和__thinRadarField对象，只显示__roundRadarField对象
        self.__largeRadarField.hide()
        self.__thinRadarField.hide()
        self.__roundRadarField.hide()

        # 设置机器人的颜色为RGB值
        self.setColor(0, 200, 100)
        # 设置枪支的颜色
        self.setGunColor(0, 200, 100)
        # 设置雷达的颜色
        self.setRadarColor(0, 200, 100)
        # 设置子弹的颜色
        self.setBulletsColor(0, 200, 100)

        # 设置变形原点：
        # radarField
        # 设置雷达领域对象的变形原点为其中心
        self.__radarField.setTransformOriginPoint(x, y)
        # 设置较大的雷达领域对象的变形原点
        self.__largeRadarField.setTransformOriginPoint(x, y)
        # 设置较窄的雷达领域对象的变形原点
        self.__thinRadarField.setTransformOriginPoint(x, y)
        # base
        # 设置基础部分图片的变形原点为其中心
        x = self.__baseWidth / 2
        y = self.__baseHeight / 2
        self.__base.setTransformOriginPoint(x, y)
        # gun
        # 设置枪支图片的变形原点为其中心
        x = self.__gunWidth / 2
        y = self.__gunHeight / 2
        self.__gun.setTransformOriginPoint(x, y)
        # radar
        # 设置雷达图片的变形原点为其中心
        x = self.__radarWidth / 2
        y = self.__radarHeight / 2
        self.__radar.setTransformOriginPoint(x, y)

        # 将自身的项目添加到项目中，以避免碰撞

        self.__items = set(
            [
                self,
                self.__base,
                self.__gun,
                self.__radar,
                self.__radarField,
                self.__largeRadarField,
                self.__thinRadarField,
                self.__roundRadarField,
            ]
        )

        # init the subclassed Bot
        self.init()

        self.__currentAnimation = []

        # self.a = time.time()

    def advance(self, i):
        """
        控制角色的行为和事件逻辑

        参数：
            i (int)：计数参数，用于特定行为的触发

        返回：
            None
        """
        # # 打印时间戳
        # if i == 1:
        #     print(time.time() - self.a)
        #     self.a = time.time()

        # 判断角色的健康状态
        if self.__health <= 0:
            self.__death()

        # 获取当前动画帧
        if self.__currentAnimation == []:
            try:
                self.__currentAnimation = self.__physics.animation.list.pop()
            except IndexError:
                # 判断动画名称
                if self.__physics.animation.name == "target":
                    try:
                        self.__physics.animation = self.__runAnimation
                        self.__currentAnimation = self.__physics.animation.list.pop()
                    except IndexError:
                        pass
                else:
                    # 停止动画
                    self.stop()
                    # 尝试播放动画
                    try:
                        self.run()
                    except:
                        # 输出错误信息
                        traceback.print_exc()
                        # 退出程序
                        exit(-1)
                    # 反转动画
                    self.__physics.reverse()
                    try:
                        # 获取当前动画帧
                        self.__currentAnimation = self.__physics.animation.list.pop()
                    except:
                        pass

        # 判断是否为指定的计数参数值
        if i == 1:
            try:
                # 获取动画指令
                command = self.__currentAnimation.pop()
                # 移动角色
                dx, dy = self.__getTranslation(command["move"])
                self.setPos(dx, dy)
                # 旋转角色
                angle = self.__getRotation(command["turn"])
                self.__base.setRotation(angle)
                # 根据锁定类型旋转枪支
                if self.__gunLock.lower() == "base":
                    self.__gun.setRotation(angle)
                if self.__radarLock.lower() == "base":
                    self.__setRadarRotation(angle)
                # 旋转枪支
                angle = self.__getGunRotation(command["gunTurn"])
                self.__gun.setRotation(angle)
                # 根据锁定类型旋转雷达
                if self.__radarLock.lower() == "gun":
                    self.__setRadarRotation(angle)
                # 旋转雷达
                angle = self.__getRadarRotation(command["radarTurn"])
                self.__setRadarRotation(angle)
                # 根据指令发射子弹
                if command["fire"] != 0:
                    self.makeBullet(command["fire"])
            except:
                pass
        else:
            # 调用传感器检测方法
            self.sensors()

            # 检测角色与墙壁的碰撞
            for item in set(self.__base.collidingItems(1)) - self.__items:
                if isinstance(item, QGraphicsRectItem):
                    # 处理与墙壁的碰撞
                    self.__wallRebound(item)
                elif isinstance(item, Robot):
                    if item.__base.collidesWithItem(self.__base):
                        # 处理与机器人的碰撞
                        self.__robotRebound(item)
                elif isinstance(item, Bullet):
                    # 处理与子弹的碰撞
                    self.__bulletRebound(item)
                elif isinstance(item, radarField):
                    if item.robot.__physics.animation.name != "target":
                        # 处理目标锁定事件
                        self.__targetSeen(item)

    ### THESE ARE THE FUNCTIONS ACCESSABLE FROM OUTSIDE ###

    # -----------------------------------------------------------Gun------------------------------------------------------
    def gunTurn(self, angle):
        """
        这个函数用来调整角色的枪支旋转角度

        参数：
            angle (int)：旋转的角度，正数表示向右旋转，负数表示向左旋转

        返回：
            None
        """
        s = 1
        if angle < 0:
            s = -1
        steps = int(s * angle / self.__physics.step)
        a = angle % self.__physics.step
        if a != 0:
            self.__physics.gunTurn.append(s * a)
        for i in range(steps):
            self.__physics.gunTurn.append(s * self.__physics.step)

    def lockGun(self, part):
        self.__gunLock = part

    def setGunColor(self, r, g, b):
        """
        设置枪支的颜色

        参数：
            r (int)：颜色的红色分量，取值范围 0 到 255
            g (int)：颜色的绿色分量，取值范围 0 到 255
            b (int)：颜色的蓝色分量，取值范围 0 到 255

        返回：
            None
        """
        color = QColor(r, g, b)
        mask = self.__gun.pixmap.createMaskFromColor(self.gunMaskColor, 1)
        p = QPainter(self.__gun.pixmap)
        p.setPen(QColor(r, g, b))
        p.drawPixmap(self.__gun.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__gun.setPixmap(self.__gun.pixmap)
        self.gunMaskColor = QColor(r, g, b)

    # ----------------------------------------------------------Base-----------------------------------------------------

    def move(self, distance):
        """
        这个函数用来移动角色

        参数：
            distance (int)：角色移动的距离，负数表示向左移动，正数表示向右移动

        返回：
            None
        """
        s = 1
        if distance < 0:
            s = -1
        steps = int(s * distance / self.__physics.step)
        d = distance % self.__physics.step
        if d != 0:
            self.__physics.move.append(s * d)
        for i in range(steps):
            self.__physics.move.append(s * self.__physics.step)

    def turn(self, angle):
        """
        控制角色的旋转行为

        参数：
            angle (int)：旋转的角度，正数表示向右旋转，负数表示向左旋转

        返回：
            None
        """
        s = 1
        if angle < 0:
            s = -1
        steps = int(s * angle / self.__physics.step)
        a = angle % self.__physics.step
        if a != 0:
            self.__physics.turn.append(s * a)
        for i in range(steps):
            self.__physics.turn.append(s * self.__physics.step)

    def setColor(self, r, g, b):
        """
        设置角色的颜色

        参数：
            r (int)：颜色的红色分量，取值范围 0 到 255
            g (int)：颜色的绿色分量，取值范围 0 到 255
            b (int)：颜色的蓝色分量，取值范围 0 到 255

        返回：
            None
        """
        color = QColor(r, g, b)
        mask = self.__base.pixmap.createMaskFromColor(self.maskColor, 1)
        p = QPainter(self.__base.pixmap)
        p.setPen(QColor(r, g, b))
        p.drawPixmap(self.__base.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__base.setPixmap(self.__base.pixmap)
        self.maskColor = QColor(r, g, b)

    # ---------------------------------------------RADAR------------------------------------------------

    def setRadarField(self, form):
        """
        设置雷达场的显示形式

        参数：
            form (str)：雷达场的显示形式，可选值为"normal"、"large"、"thin"、"round"

        返回：
            None
        """
        if form.lower() == "normal":
            self.__radarField.show()
            self.__largeRadarField.hide()
            self.__thinRadarField.hide()
            self.__roundRadarField.hide()
        if form.lower() == "large":
            self.__radarField.hide()
            self.__largeRadarField.show()
            self.__thinRadarField.hide()
            self.__roundRadarField.hide()
        if form.lower() == "thin":
            self.__radarField.hide()
            self.__largeRadarField.hide()
            self.__thinRadarField.show()
            self.__roundRadarField.hide()
        if form.lower() == "round":
            self.__radarField.hide()
            self.__largeRadarField.hide()
            self.__thinRadarField.hide()
            self.__roundRadarField.show()

    def lockRadar(self, part):
        """
        这个函数用来设置雷达的锁定部分

        参数：
            part (str)：锁定的部分，可以是"gun"或"base"，分别表示锁定枪支或基础

        返回：
            None
        """
        self.__radarLock = part

    def radarTurn(self, angle):
        """
        控制角色的雷达旋转行为

        参数：
            angle (int)：旋转的角度，正数表示向右旋转，负数表示向左旋转

        返回：
            None
        """
        s = 1
        if angle < 0:
            s = -1
        steps = int(s * angle / self.__physics.step)
        a = angle % self.__physics.step
        if a != 0:
            self.__physics.radarTurn.append(s * a)
        for i in range(steps):
            self.__physics.radarTurn.append(s * self.__physics.step)

    def setRadarColor(self, r, g, b):
        """
        设置雷达的颜色

        参数：
            r (int)：颜色的红色分量，取值范围 0 到 255
            g (int)：颜色的绿色分量，取值范围 0 到 255
            b (int)：颜色的蓝色分量，取值范围 0 到 255

        返回：
            None
        """
        color = QColor(r, g, b)
        mask = self.__radar.pixmap.createMaskFromColor(self.radarMaskColor, 1)
        p = QPainter(self.__radar.pixmap)
        p.setPen(QColor(r, g, b))
        p.drawPixmap(self.__radar.pixmap.rect(), mask, mask.rect())
        p.end()
        self.__radar.setPixmap(self.__radar.pixmap)
        self.radarMaskColor = QColor(r, g, b)

    def radarVisible(self, bol):
        """
        控制雷达图像的可见性

        参数：
            bol (bool)：True 表示显示雷达，False 表示隐藏雷达

        返回：
            None
        """

        self.__radarField.setVisible(bol)
        self.__roundRadarField.setVisible(bol)
        self.__thinRadarField.setVisible(bol)
        self.__largeRadarField.setVisible(bol)

    # ------------------------------------------------Bullets---------------------------------------

    def fire(self, power):
        """
        这个函数用来发射子弹

        参数：
            power (int)：子弹的威力

        返回：
            int：子弹的 ID
        """
        # 异步开火
        self.stop()

        # 创建子弹对象并设置其属性
        bullet = Bullet(power, self.bulletColor, self)

        # 将子弹对象添加到物理引擎的开火列表中
        self.__physics.fire.append(bullet)

        # 将子弹对象添加到物品列表中
        self.__items.add(bullet)

        # 将子弹对象作为场景中的一个项添加
        self.__parent.addItem(bullet)

        # 隐藏子弹
        bullet.hide()

        # 返回子弹的 ID
        return id(bullet)

    def makeBullet(self, bullet):
        """
        显示子弹并设置其初始位置和角度。同时，减少角色的生命值。

        参数:
            bullet (Bullet): 一个 Bullet 类的实例，表示要发射的子弹。

        返回:
            int: 子弹的 ID。

        """
        bullet.show()
        pos = self.pos()
        angle = self.__gun.rotation()
        # to find the initial position
        x = pos.x() + self.__baseWidth / 2.0
        y = pos.y() + self.__baseHeight / 2.0
        dx = -math.sin(math.radians(angle)) * self.__gunWidth / 2.0
        dy = math.cos(math.radians(angle)) * self.__gunHeight / 2.0
        pos.setX(x + dx)
        pos.setY(y + dy)
        bot = self
        bullet.init(pos, angle, self.__parent)

        self.__changeHealth(self, -bullet.power)
        return id(bullet)

    def setBulletsColor(self, r, g, b):
        """
        这个函数用来设置子弹的颜色

        参数：
            r (int)：颜色的红色分量，取值范围 0 到 255
            g (int)：颜色的绿色分量，取值范围 0 到 255
            b (int)：颜色的蓝色分量，取值范围 0 到 255

        返回：
            None
        """
        self.bulletColor = QColor(r, g, b)

    # ---------------------------------------General Methods---------------------------------------
    def stop(self):
        """
        这个函数用来停止角色的当前动作

        参数：无

        返回：None
        """
        self.__physics.newAnimation()

    def getMapSize(self):
        """
        获取地图的大小

        参数：无

        返回值：
            tuple：一个二元组，表示地图的大小，格式为 (宽, 高)

        返回值示例：
            (1000, 800)
        """
        return self.__mapSize

    def getPosition(self):
        """
        获取角色的中心位置

        参数：
            无

        返回值：
            QPointF：一个 QPointF 对象，表示角色的中心位置，坐标以游戏窗口为准

        返回值示例：
            QPointF(150.0, 200.0)
        """
        p = self.pos()
        r = self.__base.boundingRect()
        return QPointF(p.x() + r.width() / 2, p.y() + r.height() / 2)

    def getGunHeading(self):
        """
        这个函数用来获取枪支的朝向角度

        参数：
            无

        返回值：
            float：枪支的朝向角度，单位为度

        返回值示例：
            30.5
        """
        angle = self.__gun.rotation()
        # if angle > 360:
        #     a = int(angle) / 360
        #     angle = angle - (360*a)
        return angle

    def getHeading(self):
        """
        获取角色基础部分的旋转角度。

        返回值：
            float：角色基础部分的旋转角度，单位为度。

        返回值示例：
            45.0
        """
        return self.__base.rotation()

    def getRadarHeading(self):
        """
        这个函数用来获取雷达的朝向角度

        参数：
            无

        返回值：
            float：雷达的朝向角度，单位为度

        返回值示例：
            30.5
        """
        return self.__radar.rotation()

    def reset(self):
        """
        这个函数用来重置角色的状态

        参数：
            无

        返回值：
            无

        使用示例：
            >>> a.reset()
        """
        self.__physics.reset()
        self.__currentAnimation = []

    def getEnemiesLeft(self):
        """
        这个函数用来获取当前场景中所有存活的敌人信息

        参数：
            无

        返回值：
            list：一个列表，包含所有存活的敌人的 ID 和名称

        返回值示例：
            [{'id': 1, 'name': '敌人1'}, {'id': 2, 'name': '敌人2'}]
        """
        l = []
        for bot in self.__parent.aliveBots:
            dic = {"id": id(bot), "name": bot.__repr__()}
            l.append(dic)
        return l

    def rPrint(self, msg):
        """
        这个函数用来打印错误信息

        参数：
            msg (str)：要打印的错误信息

        返回值：
            无

        使用示例：
            >>> self.rPrint("出错了！")
        """
        self.info.out.add(str(msg))

    def pause(self, duration):
        """
        这个函数用来暂停角色的移动

        参数：
            duration (int)：暂停的时间，单位为秒

        返回值：
            None

        使用示例：
            >>> self.pause(5)
        """
        self.stop()
        for i in range(int(duration)):
            self.__physics.move.append(0)
        self.stop()

    # END: g5lm5vp8jcu6

    ###end of functions accessable from outside###

    # Calculus & Private Methods
    def __getTranslation(self, step):
        """
        这个函数用来根据角色的当前角度和给定的步长，计算出角色在水平和垂直方向上的位移量

        参数:
            step (int)：角色移动的步长

        返回值：
            tuple：一个二元组，表示角色在 x 和 y 方向上的位移量，格式为 (dx, dy)

        返回值示例：
            (150.0, -200.0)
        """
        angle = self.__base.rotation()
        pos = self.pos()
        x = pos.x()
        y = pos.y()
        dx = -math.sin(math.radians(angle)) * step
        dy = math.cos(math.radians(angle)) * step
        # print(dx, dy)
        return x + dx, y + dy

    def __setRadarRotation(self, angle):
        """
        这个函数用来设置角色的雷达及相关组件的旋转角度

        参数：
            angle (float)：雷达及相关组件需要设置的旋转角度

        返回值：
            无

        返回值示例：
            无
        """
        self.__radar.setRotation(angle)
        self.__radarField.setRotation(angle)
        self.__largeRadarField.setRotation(angle)
        self.__thinRadarField.setRotation(angle)

    def __getRotation(self, alpha):
        """
        这个函数用来根据角色的当前角度和给定的旋转角度增量计算新的旋转角度

        参数:
            alpha (float)：旋转角度的增量

        返回值：
            float：角色旋转后的角度

        使用示例：
            >>> new_angle = __getRotation(30.0)
        """
        return self.__base.rotation() + alpha

    def __getGunRotation(self, alpha):
        """
        这个函数用来获取角色武器旋转后的角度

        参数：
            alpha (float)：旋转角度的增量

        返回值：
            float：角色武器旋转后的角度

        使用示例：
            >>> new_angle = __getGunRotation(30.0)
        """
        return self.__gun.rotation() + alpha

    def __getRadarRotation(self, alpha):
        """
        获取雷达旋转角度

        参数：
            alpha (float)：旋转角度的增量

        返回值：
            float：雷达旋转后的角度
        """
        return self.__radar.rotation() + alpha

    def __wallRebound(self, item):
        """
        这个函数用来处理角色与墙壁碰撞后的反弹逻辑

        参数：
            item (QGraphicsItem)：与角色碰撞的墙壁 GraphicsItem

        返回值：
            无

        使用示例：
            >>> self.__wallRebound(wall_item)
        """
        self.reset()
        if item.name == "left":
            x = self.__physics.step * 1.1
            y = 0
        elif item.name == "right":
            x = -self.__physics.step * 1.1
            y = 0
        elif item.name == "top":
            x = 0
            y = self.__physics.step * 1.1
        elif item.name == "bottom":
            x = 0
            y = -self.__physics.step * 1.1
        self.setPos(self.pos().x() + x, self.pos().y() + y)
        self.__changeHealth(self, -1)
        self.stop()
        try:
            self.onHitWall()
        except:
            traceback.print_exc()
            exit(-1)
        animation = self.__physics.makeAnimation()
        if animation != []:
            self.__currentAnimation = animation

    def __robotRebound(self, robot):
        """
        这个函数用来处理角色与机器人碰撞后的反弹逻辑

        参数：
            robot (QGraphicsItem)：与角色碰撞的机器人 GraphicsItem

        返回值：
            无

        使用示例：
            >>> self.__robotRebound(robot_item)
        """
        try:
            self.reset()
            robot.reset()
            angle = self.__base.rotation()
            pos = self.pos()
            x = pos.x()
            y = pos.y()
            dx = -math.sin(math.radians(angle)) * self.__physics.step * 1.1
            dy = math.cos(math.radians(angle)) * self.__physics.step * 1.1
            self.setPos(x - dx, y - dy)
            pos = robot.pos()
            x = pos.x()
            y = pos.y()
            robot.setPos(x + dx, y + dy)
            self.__changeHealth(robot, -1)
            self.__changeHealth(self, -1)
            self.stop()
            self.onRobotHit(id(robot), robot.__repr__())
            animation = self.__physics.makeAnimation()
            if animation != []:
                self.__currentAnimation = animation
            robot.stop()
            robot.onHitByRobot(id(self), self.__repr__())
            animation = robot.__physics.makeAnimation()
            if animation != []:
                robot.__currentAnimation = animation
        except:
            traceback.print_exc()
            exit(-1)

    def __bulletRebound(self, bullet):
        """
        这个函数用来处理角色与子弹碰撞后的反弹逻辑

        参数：
            bullet (BulletItem)：与角色碰撞的子弹 GraphicsItem

        返回值：
            无

        使用示例：
            >>> self.__bulletRebound(bullet_item)
        """
        # 根据子弹的威力改变角色的健康值
        self.__changeHealth(self, -3 * bullet.power)

        try:
            # 检查子弹的发射者机器人是否存活
            if bullet.robot in self.__parent.aliveBots:
                # 如果存活，根据子弹的威力改变机器人的健康值
                self.__changeHealth(bullet.robot, 2 * bullet.power)

            # 停止角色的移动
            self.stop()

            # 触发角色被子弹击中的事件，并传递子弹的机器人ID、机器人名称和子弹威力的信息
            self.onHitByBullet(id(bullet.robot), bullet.robot.__repr__(), bullet.power)

            # 创建角色被击中后的动画效果，并将其设置为当前动画
            animation = self.__physics.makeAnimation()
            if animation != []:
                self.__currentAnimation = animation

            # 停止子弹的发射者机器人的移动
            bullet.robot.stop()
            # 触发发射者机器人被子弹击中的事件，并传递角色ID和子弹ID
            bullet.robot.onBulletHit(id(self), id(bullet))
            # 创建子弹的发射者机器人被子弹击中后的动画效果，并将其设置为当前动画
            animation = bullet.robot.__physics.makeAnimation()
            if animation != []:
                bullet.robot.__currentAnimation = animation

            # 从场景中移除子弹
            self.__parent.removeItem(bullet)
        except:
            # 忽略可能发生的异常
            pass

    def __targetSeen(self, target):
        """
        这个函数用来处理角色发现目标后的逻辑

        参数：
            target (QGraphicsItem)：被发现的目标 GraphicsItem

        返回值：
            无

        使用示例：
            >>> self.__targetSeen(target_item)
        """
        self.stop()
        anim = target.robot.__currentAnimation
        target.robot.__physics.animation = target.robot.__targetAnimation
        target.robot.__physics.reset()
        try:
            target.robot.onTargetSpotted(id(self), self.__repr__(), self.getPosition())
        except:
            traceback.print_exc()
            exit(-1)
        target.robot.__physics.newAnimation()
        target.robot.__physics.reverse()
        try:
            target.robot.__currentAnimation = (
                target.robot.__physics.animation.list.pop()
            )
        except:
            target.robot.__physics.animation = target.robot.__runAnimation
            target.robot.__currentAnimation = anim

    def __changeHealth(self, bot, value):
        """
        这个函数用来改变机器人的健康值，并在必要时更新进度条

        参数：
            bot (RobotItem)：目标机器人
            value (int)：健康值的改变量，可以是正数或负数

        返回值：
            无

        使用示例：
            >>> self.__changeHealth(robot, -10)  # 将 robot 的健康值减少 10
        """
        bot.__health += value
        if bot.__health > 100:
            bot.__health = 100
        elif bot.__health < 0:
            bot.__health = 0
        try:
            bot.progressBar.setValue(bot.__health)
        except:
            pass

    def removeMyProtectedItem(self, item):
        """
        这个函数用来从列表中移除一个受保护的项目

        参数：
            item (any)：需要从列表中移除的项目

        返回值：
            无

        使用示例：
            >>> removeMyProtectedItem(self.my_list(, 'item_name'))
        """
        self.__items.remove(item)

    def __death(self):
        """
        这个函数用来处理角色的死亡逻辑

        参数：
            无

        返回值：
            无

        使用示例：
            >>> self.__death()
        """
        try:
            self.icon.setIcon(QIcon(os.getcwd() + "/robotImages/dead.png"))
            self.icon2.setIcon(QIcon(os.getcwd() + "/robotImages/dead.png"))
            self.progressBar.setValue(0)
        except:
            pass
        self.__parent.deadBots.append(self)
        self.__parent.aliveBots.remove(self)
        try:
            self.onRobotDeath()
        except:
            traceback.print_exc()
            exit(-1)
        self.__parent.removeItem(self)
        if len(self.__parent.aliveBots) <= 1:
            self.__parent.battleFinished()

    def __repr__(self):
        """
        返回对象的字符串表示

        这个方法用于定义对象的字符串表示，当使用内置函数 repr() 对对象进行操作时，会调用这个方法

        返回值：
            str：对象的字符串表示

        返回值示例：
            'MyClass(1, "example")'
        """
        repr = self.__repr.split(".")
        return repr[1].replace("'>", "")
