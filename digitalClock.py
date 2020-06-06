#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QTime, QTimer, QDate, Qt
from PyQt5.QtWidgets import QApplication,  QLabel, QWidget, QGridLayout, QVBoxLayout, QSizePolicy
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QFontMetrics
import config


class DigitalClock(QWidget):
    def __init__(self, width=None, parent=None):
        width_to_height = 4 / 3
        super(DigitalClock, self).__init__(parent)
        
        self.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Maximum
        )

        ##Clock Part
        self.hmLabel = QLabel("88:88")
        self.sLabel = QLabel("88")
        self.ampmLabel = QLabel("PM")
        self.clockLayout = QGridLayout()
        self.setStyleSheet("background-color: black")
        if width is not None:
            self.w = width
            self.h = self.w / width_to_height
            self.resize(self.w, self.h)

        #width, height
        self.hmLabel.resize(int(self.width() * 2 / 3), int(self.width() / width_to_height* 4/12)) #time takes up 2/3 height
        self.ampmLabel.resize(int(self.width() / 3), int(self.width() / width_to_height /2 * 4/12))
        self.sLabel.resize(int(self.width() / 3), int(self.width() / width_to_height /2 * 4/ 12))

        self.clockLayout.addWidget(self.hmLabel, 1, 1, 2, 4, QtCore.Qt.AlignRight)
        self.clockLayout.addWidget(self.ampmLabel, 1, 5, 1, 2, QtCore.Qt.AlignLeft)
        self.clockLayout.addWidget(self.sLabel, 2, 5, 1, 2, QtCore.Qt.AlignLeft)

        #Date Part
        self.dateLabel = QLabel("December 31, 2088")
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dayOfWeekLabel = QLabel("Wednesday")
        self.dayOfWeekLabel.setAlignment(QtCore.Qt.AlignCenter)
        today = QDate.currentDate()
        dayofWeek = today.longDayName(today.dayOfWeek())

        date = str(today.toString(Qt.DefaultLocaleLongDate))
        numLettersInDay = len(dayofWeek)
        date = date[numLettersInDay + 1:]


        #self.dateLabel.setText(str(today.toString(Qt.DefaultLocaleLongDate)))
        self.dateLabel.setText(date)
        self.dayOfWeekLabel.setText(str(dayofWeek))
        self.dateLabel.resize(int(self.width()), int(self.width() / width_to_height * 3/12))
        self.dayOfWeekLabel.resize(int(self.width()), int(self.width() / width_to_height * 5/12))

        self.dateAndTimeLayout = QVBoxLayout()
        self.dateAndTimeLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.dateAndTimeLayout.addWidget(self.dayOfWeekLabel, QtCore.Qt.AlignCenter)
        self.dateAndTimeLayout.addWidget(self.dateLabel, QtCore.Qt.AlignCenter)
        self.dateAndTimeLayout.addLayout(self.clockLayout)

        for item in self.hmLabel, self.ampmLabel, self.sLabel, self.dateLabel, self.dayOfWeekLabel:
            item.setFont(self.getFont(item.text(), item))
            item.setStyleSheet(config.font_colour)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.setLayout(self.dateAndTimeLayout)
        self.showTime()

    def showTime(self):
        time = QTime.currentTime()
        hour = time.hour()
        ampm = ""
        if hour > 12:
            ampm = "PM"
            hour = hour - 12
        else:
            ampm = "AM"
        minute = time.minute()
        if minute >= 10:
            minutestr = str(minute)
        else:
            minutestr = "0" + str(minute)
        second = time.second()
        if second >= 10:
            secondstr = str(second)
        else:
            secondstr = "0" + str(second)

        self.hmLabel.setText(str(hour) + ":" + minutestr)
        self.sLabel.setText(secondstr)
        self.ampmLabel.setText(ampm)

    def getFont(self, text, rect):
        font = QFont()
        cr = rect.contentsRect()

        # --- find the font size that fits the contentsRect ---
        fs = 1
        while True:
            font.setPointSize(fs)
            br = QFontMetrics(font).boundingRect(text)
            if br.height() <= cr.height() and br.width() <= cr.width():
                fs += 1
            else:
                wouldfit = max(fs - 6, 1)
                font.setPointSize(wouldfit)
                break
        font.setFamily(config.font_family)
        font.setBold(1)
        return font


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())
