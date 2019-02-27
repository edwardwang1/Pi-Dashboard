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
                             QHBoxLayout, QVBoxLayout, QApplication, QGridLayout, QLabel, QDesktopWidget)
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui
import Pyro4
import threading

import weather, digitalClock, analogClock

@Pyro4.expose
class Example(QWidget):
    shutdownSignal = pyqtSignal()
    

    def __init__(self, daemon):
        super().__init__()
        self.daemon = daemon
        self.initUI()

    def initUI(self):
        #blueButton = QPushButton("Blue")
        #blueButton.clicked.connect(self.change_background_to_blue)
        #redButton = QPushButton("Red")
        #redButton.clicked.connect(self.change_background_to_red)


        
        self.shutdownSignal.connect(self.closeProgram)
        #self.showFullScreen()
        #self.showNormal()
        desktopSize = QDesktopWidget().screenGeometry()
        desktopWidth = desktopSize.width()
        desktopHeight = desktopSize.height()
        self.showFullScreen()
        
        if desktopWidth > desktopHeight: 
            self.resize(1500, 2000)
        else:
            self.resize(desktopWidth, desktopHeight)

        print(self.width(), self.height())
        
        desktopSize = QDesktopWidget().screenGeometry()


        self.aClock = analogClock.PyAnalogClock(parent=self, width=self.width()/1.2)
        self.weath = weather.Weather(parent=self, width=self.width()/6)
        #print("weath", self.weath.width())
        self.dClock = digitalClock.DigitalClock(parent=self, width=self.width()/4)
        #print(self.dClock.width(), self.dClock.height())

        self.dClock.showFullScreen()

        ## Moving widgets to proper locatoin, (from top, from left)
        self.weath.move(int(self.width()/20), int(self.width()/20))
        self.weath.resizeComponents()

        self.dClock.move(self.width() - int(self.width()/20) - self.dClock.width(), int(self.width()/20))
        self.aClock.move(int(self.width()/2 - self.aClock.width()/2), int(self.height()/2 - self.aClock.width()/2))


    
        self.setStyleSheet("background-color:black")

        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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
