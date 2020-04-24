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
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QGridLayout, QLabel, QDesktopWidget)
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui
import Pyro4
import threading
import atexit

import weather, digitalClock, googleCalendar


class Example(QWidget):
    shutdownSignal = pyqtSignal()


    def __init__(self, daemon):
        super().__init__()
        self.daemon = daemon
        self.initUI()

    def initUI(self):
        self.shutdownSignal.connect(self.closeProgram)
        desktopSize = QDesktopWidget().screenGeometry()
        desktopWidth = desktopSize.width()
        desktopHeight = desktopSize.height()
        self.showFullScreen()

        if desktopWidth > desktopHeight:
            self.resize(1050/1.5, 1680/1.5)
        else:
            self.resize(desktopWidth, desktopHeight)

        self.weath = weather.Weather(parent=self, width=self.width()/6)
        self.dClock = digitalClock.DigitalClock(parent=self, width=self.width()/4)

        self.calendar = googleCalendar.GoogleCalendar(parent=self, width=self.width() /6)
        self.dClock.showFullScreen()

        ## Moving widgets to proper locatoin, (from top, from left)
        self.weath.move(int(self.width()/20), int(self.width()/20))
        self.weath.resizeComponents()
        self.dClock.move(self.width() - int(self.width()/20) - self.dClock.width(), int(self.width()/20))
        self.calendar.move(int(self.width()/20), int(self.width()/20) + self.weath.height() + int(self.width()/10))
        self.calendar.update()
        #self.aClock.move(int(self.width()/2 - self.aClock.width()/2), int(self.height()/2 - self.aClock.width()/2))


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

    @Pyro4.expose
    @Pyro4.oneway
    def shutdown(self):
        self.daemon.shutdown()
        self.shutdownSignal.emit()
        
    def closeProgram(self):
        print("closing")
        sys.exit()


def establishingPyroServer(sharedObj):
    
    uri = daemon.register(sharedObj)
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


atexit.register(wipeUriFile)


if __name__ == '__main__':
    print("begin")
    daemon = Pyro4.Daemon()
    app = QApplication(sys.argv)
    ex = Example(daemon)
    t = PyroThread(ex)
    t.setDaemon(True)
    t.start()
    sys.exit(app.exec_())
