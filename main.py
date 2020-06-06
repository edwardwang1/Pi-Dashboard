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
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QGridLayout, QLabel, QDesktopWidget, QMainWindow, QLayout)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtCore, QtGui
import Pyro4
import threading
import atexit
from mycroft_bus_client import MessageBusClient, Message
import os
from PyQt5.QtWidgets import QGridLayout
import weather, digitalClock, googleCalendar, commandDisplay, notes

class Example(QWidget):
    shutdownSignal = pyqtSignal()
    signalAddNote = QtCore.pyqtSignal()
    signalRemoveNote = QtCore.pyqtSignal() 

    def __init__(self, daemon):
        super().__init__()
        self.daemon = daemon
        self.thread = QtCore.QThread()
        self.initUI()

    def initUI(self):    
        self.shutdownSignal.connect(self.closeProgram)
        desktopSize = QDesktopWidget().screenGeometry()
        desktopWidth = desktopSize.width()
        desktopHeight = desktopSize.height()
        self.showFullScreen()

        self.setStyleSheet("background-color:black")

        if desktopWidth > desktopHeight:
            self.resize(1050/1.5, 1680/1.5)
        else:
            self.setFixedSize(desktopWidth, desktopHeight)

        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(0)

        self.weath = weather.Weather(parent=self, width=self.width()/5)
        self.dClock = digitalClock.DigitalClock(parent=self, width=self.width()/4)
        self.calendar = googleCalendar.GoogleCalendar(parent=self, width=self.width() /4)
        self.dClock.showFullScreen()
        self.notes = notes.Notes(parent=self, width=self.width() / 4, align="right")
        self.commandDisplay = commandDisplay.CommandDisplay(parent=self, width=self.width() / 4)
        
        #addWidget(object, row, column)
        self.layout.addWidget(self.weath, 1, 0, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.dClock, 1, 2, alignment=Qt.AlignRight)
        self.layout.addWidget(self.calendar, 3, 0, alignment=(Qt.AlignLeft | Qt.AlignTop))
        self.layout.addWidget(self.notes, 3, 2, alignment=(Qt.AlignRight | Qt.AlignTop))
        self.layout.addWidget(self.commandDisplay, 4, 1, alignment=(Qt.AlignCenter|Qt.AlignBottom))

        self.layout.setRowMinimumHeight(0, self.height()/25)
        self.layout.setRowMinimumHeight(2, self.height()/25)
        self.layout.setRowMinimumHeight(5, self.height()/25)
         
        self.layout.setColumnMinimumWidth(0, self.width()/4)
        self.layout.setColumnMinimumWidth(1, self.width()/2)
        self.layout.setColumnMinimumWidth(2, self.width()/4)
                       
        self.setLayout(self.layout)
        self.show()
                
        #Signals
        self.signalAddNote.connect(self.notes.addNote)
        self.signalRemoveNote.connect(self.notes.removeNote)
    
    
    ##Connecting to Mycroft
    @Pyro4.expose
    @Pyro4.oneway
    def showHideAllWidgets(self, vis):
        self.showHideCalendar(vis)
        self.showHideClock(vis)
        self.showHideWeather(vis)
        self.showHideCommandDisplay(vis)
        self.showHideNotes(vis)
    
    @Pyro4.expose
    @Pyro4.oneway
    def showHideCalendar(self, vis):
        self.calendar.setVisible(vis)
        
    @Pyro4.expose
    @Pyro4.oneway
    def showHideClock(self, vis):
        self.dClock.setVisible(vis)
        
    @Pyro4.expose
    @Pyro4.oneway
    def showHideWeather(self, vis):
        self.weath.setVisible(vis)
        
    @Pyro4.expose
    @Pyro4.oneway
    def showHideCommandDisplay(self, vis):
        self.commandDisplay.setVisible(vis)
        
    @Pyro4.expose
    @Pyro4.oneway
    def showHideNotes(self, vis):
        self.notes.setVisible(vis)

    @Pyro4.expose
    @Pyro4.oneway
    def updateCommandDisplay(self, text):
        self.commandDisplay.inputLabel.setText(text)
        
    @Pyro4.expose
    @Pyro4.oneway
    def addNote(self, text):
        self.thread.start()
        self.notes.incomingText = text
        self.signalAddNote.emit()
        
    @Pyro4.expose
    @Pyro4.oneway
    def removeNote(self, text):
        self.thread.start()
        self.notes.incomingText = text
        self.signalRemoveNote.emit()

    @Pyro4.expose
    @Pyro4.oneway
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
    #if sys.platform == "linux" or platform == "linux2":
        #os.system('/usr/bin/python3 ~/Desktop/RPiDashboard/messageBus.py')
