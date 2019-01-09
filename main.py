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
from PyQt5.QtCore import pyqtSignal                             
import Pyro4
import threading

@Pyro4.expose
class Example(QWidget):
    shutdownSignal = pyqtSignal()
    

    def __init__(self, daemon):
        super().__init__()
        self.daemon = daemon
        self.initUI()

    def initUI(self):
        blueButton = QPushButton("Blue")
        blueButton.clicked.connect(self.change_background_to_blue)
        redButton = QPushButton("Red")
        redButton.clicked.connect(self.change_background_to_red)
        
        self.shutdownSignal.connect(self.closeProgram)

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

    def change_background_to_blue(self):
        self.setStyleSheet("background-color: blue;")
        print("test")
        exitWhenFalse = 0


    def change_background_to_red(self):
        self.setStyleSheet("background-color: red;")
        print("Test2")

    def empty(self):
        pass
        
    @Pyro4.oneway
    def shutdown(self):
        self.daemon.shutdown()
        self.shutdownSignal.emit()

        
    def closeProgram(self):
        print("closing")
        sys.exit()


def establishingPyroServer(sharedObj):
    
    uri = daemon.register(sharedObj)
    print(uri)
    #text_file = open("C:\\Users\\Edward\\Desktop\\Output.txt", "w")
    text_file = open("uri.txt", "w")
    text_file.write(str(uri))
    text_file.close()
    daemon.requestLoop()
    daemon.close()

 
def wipeUriFile():
    text_file = open("uri.txt", "w")
    text_file.write("")
    text_file.close()
    

class PyroThread(threading.Thread):
    def __init__(self, shared, *args, **kwargs):
        super(PyroThread, self).__init__(*args, **kwargs)
        self.shared = shared

    def run(self):
        establishingPyroServer(self.shared)

import atexit
atexit.register(wipeUriFile)


if __name__ == '__main__':
    daemon = Pyro4.Daemon()
    app = QApplication(sys.argv)
    ex = Example(daemon)
    t = PyroThread(ex)
    t.setDaemon(True)
    t.start()
    sys.exit(app.exec_())
