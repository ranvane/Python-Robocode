# -*- coding: utf-8 -*-

"""
Module implementing RobotInfo.
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot

from outPrint import outPrint
from Ui_RobotInfo import Ui_Form

class RobotInfo(QWidget, Ui_Form):
    """
    定义 RobotInfo 类，继承自 QWidget 和 Ui_Form 类
    """
    def __init__(self, parent = None):
        """
        构造函数，初始化父类和界面

        参数：
            parent (QWidget)：父窗口对象，默认为 None
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.out = outPrint()
        # 初始化一个 outPrint 对象，用于显示信息

    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        定义槽函数，当 pushButton 被点击时显示 out 窗口

        """
        
        self.out.setWindowTitle(str(self.robot))
        self.out.show()
        # 设置 outPrint 对象的窗口标题为 robot 的字符串表示，并显示 outPrint 窗口
    
    @pyqtSlot(int)
    def on_progressBar_valueChanged(self, value):
        """
        定义槽函数，当 progressBar 的值发生变化时，更新 progressBar 的样式

        参数：
            value (int)：进度条的当前值
        """
        
        value -= 7
        if value <=0:
            value = 0
        if value >= 50:
            green = 255
            red = int(510 - (value*2)*2.55)
        else:
            red = 255
            green = int((value*2)*2.55)
        self.progressBar.setStyleSheet("""
        QProgressBar {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
        height: 5px;
        }
        QProgressBar::chunk {
        background-color: rgb(""" + str(red) + "," + str(green) + """,0);
        }
        """)
        # 根据进度条的值计算红色和绿色的值，然后更新 progressBar 的样式，设置背景颜色
