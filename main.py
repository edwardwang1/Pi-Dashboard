#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we position two push
buttons in the bottom-right corner
of the window.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        blueButton = QPushButton("Blue")
        blueButton.clicked.connect(self.on_click)
        redButton = QPushButton("Red")
        redButton.clicked.connect(self.on_click_red)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(blueButton)
        hbox.addWidget(redButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()

    def on_click(self):
        self.setStyleSheet("background-color: blue;")

    def on_click_red(self):
        self.setStyleSheet("background-color: red;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())