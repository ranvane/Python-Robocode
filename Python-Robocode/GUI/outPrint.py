# -*- coding: utf-8 -*-

"""
Module implementing outPrint.
"""

from PyQt5.QtWidgets import QWidget

from Ui_outPrint import Ui_Form

class outPrint(QWidget, Ui_Form):
    """
    允许外部代码将消息传递给outPrint类，并将这些消息显示在textEdit控件中。
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)

        
    def add(self, msg):
        self.textEdit.append(msg)
