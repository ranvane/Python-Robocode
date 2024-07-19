#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

# 获取当前脚本的路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 计算父文件夹的父文件夹的路径
parent_path = os.path.dirname(current_path)

# 将父文件夹的父文件夹的路径添加到 Python 的搜索路径中
sys.path.append(parent_path)
sys.path.append(os.path.join(parent_path, "Objects"))
try:
    from robot import Robot  # 导入一个名为Robot的基类
except Exception as e:

    from Objects.robot import Robot


from loguru import logger
import time, random


class Test_Demo(Robot):  # 创建一个名为Demo的机器人，继承自Robot类

    def init(self):  # 初始化方法，用于设置机器人的初始状态
        """
        初始化机器人的颜色和显示设置

        参数：
            self：对象引用

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.init()
        """
        # print(dir(self))
        logger.info("初始化机器人")
        # 设置机器人颜色
        self.setColor(0, 200, 100)
        # 设置机器人枪支颜色
        self.setGunColor(200, 200, 0)
        # 设置机器人雷达颜色
        self.setRadarColor(255, 60, 0)
        # 设置机器人子弹颜色
        self.setBulletsColor(0, 200, 100)

        # 获取地图大小
        size = self.getMapSize()
        # 显示雷达场
        self.radarVisible(True)
        self.lockRadar(True)

    def run(self):  # 运行方法，是机器人行为的主要逻辑
        """
        机器人的运行逻辑

        参数：
            self：对象引用

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.run()
        """
        try:
            s = random.randint(30, 100)
            logger.info("机器人运行中...")
            logger.info(f"机器人前进{s}步")
            self.move(s)  # 前进90步（负数为后退）
        except Exception as e:
            logger.info(e)

        # self.turn(360)  # 车体旋转360°（负数为逆时针旋转）
        # self.stop()
        """
        此处的stop命令用于执行移动序列：机器人将同时移动90步并旋转360°
        然后，进行开火
        """

        # self.fire(3)  # 开火（威力介于1到10之间）

        # self.move(100)
        # self.turn(50)
        # self.stop()
        # # 记录开火的子弹ID，方便管理子弹的命中与否
        # bulletId = self.fire(2)

        # self.move(180)
        # self.turn(180)
        # self.gunTurn(90)
        # self.stop()
        # self.fire(1)

        # self.radarTurn(90)

        # self.stop()

    def get_sensors(self):  # 传感器方法，用于获取游戏状态数据
        """
        调用此方法，以获取游戏信息

        参数：
            self：对象引用

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.sensors()
        """
        pos = self.getPosition()  # 获取机器人的当前位置，返回值是一个包含x和y坐标的对象
        x = pos.x()  # 获取x坐标
        y = pos.y()  # 获取y坐标

        # 获取机器人的枪口朝向
        GunHead_Angle = self.getGunHeading()
        # 获取机器人的朝向
        Head_Angle = self.getHeading()
        # 获取机器人的雷达朝向
        RadarHead_Angle = self.getRadarHeading()
        # 获取存活的敌人列表
        list = self.getEnemiesLeft()
        # for robot in list:
        #     id = robot["id"]
        #     name = robot["name"]
        #     # 列表中的每个元素都是一个字典，包含机器人的id和名称
        # self.rPrint(
        #     f"机器人位置：x:{x} y:{y}\n机器人枪口朝向：{GunHead_Angle}\n机器人朝向：{Head_Angle}\n机器人雷达：{RadarHead_Angle}"
        # )
        logger.info(
            f"地图大小{self.getMapSize()}\n机器人位置：x:{x} y:{y}\n机器人枪口朝向：{GunHead_Angle}\n机器人朝向：{Head_Angle}\n机器人雷达：{RadarHead_Angle}"
        )

    def sensors(self):  # 传感器方法，用于获取游戏状态数据
        """
        每一帧更新时调用此方法，以获取游戏信息

        参数：
            self：对象引用

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.sensors()
        """
        pos = self.getPosition()  # 获取机器人的当前位置，返回值是一个包含x和y坐标的对象
        x = pos.x()  # 获取x坐标
        y = pos.y()  # 获取y坐标

        # 获取机器人的枪口朝向
        GunHead_Angle = self.getGunHeading()
        # 获取机器人的朝向
        Head_Angle = self.getHeading()
        # 获取机器人的雷达朝向
        RadarHead_Angle = self.getRadarHeading()
        # 获取存活的敌人列表
        list = self.getEnemiesLeft()
        # for robot in list:
        #     id = robot["id"]
        #     name = robot["name"]
        #     # 列表中的每个元素都是一个字典，包含机器人的id和名称
        # self.rPrint(
        #     f"机器人位置：x:{x} y:{y}\n机器人枪口朝向：{GunHead_Angle}\n机器人朝向：{Head_Angle}\n机器人雷达：{RadarHead_Angle}"
        # )
        # logger.info(
        #     f"机器人位置：x:{x} y:{y}\n机器人枪口朝向：{GunHead_Angle}\n机器人朝向：{Head_Angle}\n机器人雷达：{RadarHead_Angle}"
        # )

    def onHitByRobot(self, robotId, robotName):
        """
        当机器人被另一个机器人碰撞时调用此方法

        参数：
            self：对象引用
            robotId：碰撞机器人的ID
            robotName：碰撞机器人的名称

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.onHitByRobot(1, "enemy_robot")
        """
        logger.info(f"机器人id:{robotId} Name :{robotName}碰撞了我!")

    def onHitWall(self):
        """
        当机器人撞到墙壁时调用此方法

        参数：
            self：对象引用

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.onHitWall()
        """
        # 重置运行函数到开头
        self.reset()
        # self.pause(100)
        # 向后移动100步（负数表示向后）
        s = random.randint(-100, -30)
        logger.info(f"撞到墙了!机器人运行{s}步")
        self.move(s)

        # # 改变雷达场的形式
        # self.setRadarField("large")
        self.get_sensors()

    def onRobotHit(self, robotId, robotName):
        """
        当我的机器人撞到另一个机器人时调用此方法

        参数：
            self：对象引用
            robotId：被撞机器人的ID
            robotName：被撞机器人的名称

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.onRobotHit(1, "enemy_robot")
        """
        logger.info(f"我和:{robotName}碰撞！")

    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower):
        """
        当我被一颗子弹击中时调用此方法

        参数：
            self：对象引用
            bulletBotId：射击子弹的机器人ID
            bulletBotName：射击子弹的机器人名称
            bulletPower：子弹的威力

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.onHitByBullet(1, "enemy_robot", 5)
        """
        # 重置运行函数到开头
        self.reset()
        logger.info(f"我被{bulletBotName}的子弹击中了，威力：{bulletPower}！")

    def onBulletHit(self, botId, bulletId):
        """
        当我的子弹击中一个机器人时调用此方法

        参数：
            self：对象引用
            botId：被击中的机器人ID
            bulletId：击中机器人的子弹ID

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.onBulletHit(1, 2)
        """
        logger.info(f"我击中了：{botId}")

    def onBulletMiss(self, bulletId):
        """
        当我的子弹打偏时调用此方法

        参数：
            self：对象引用
            bulletId：打偏的子弹ID

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.onBulletMiss(1)
        """
        logger.info(f"我的子弹：{bulletId}打偏了！")
        # 等待10帧
        self.pause(10)

    def onRobotDeath(self):
        """
        当我的机器人死亡时调用此方法

        参数：
            self：对象引用

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.onRobotDeath()
        """
        self.rPrint("机器人死亡")

    def onTargetSpotted(self, botId, botName, botPos):
        """
        当我的机器人发现另一个目标时调用此方法

        参数：
            self：对象引用
            botId：目标机器人的ID
            botName：目标机器人的名称
            botPos：目标机器人的位置（包含x和y坐标的对象）

        返回值：
            无

        调用示例：
            robot = MyRobot()
            robot.onTargetSpotted(1, "enemy_robot", Position(10, 20))
        """
        # 开火威力5
        self.fire(5)
        logger.info(f"发现另一个目标,id:{botId} 位置：({botPos.x()},{botPos.y()})")


if __name__ == "__main__":
    robot = Test_Demo()
    robot.run()
