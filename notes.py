from __future__ import print_function
import config

from PyQt5.QtCore import QTimer, Qt, QModelIndex
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QSizePolicy, QLayout, QListWidget, QListWidgetItem, QFrame
from PyQt5.QtGui import QFont, QFontMetrics

class Notes(QWidget):
    def sizeHint(self):
        return(self.size())


    def __init__(self, width=None, parent=None, align=None, titleText="Title", bodyText = "Body"):
        self.width_to_row_height = config.width_to_row_height
        super(Notes, self).__init__(parent)
        self.incomingText = ""
        self.row_height = self.width() / self.width_to_row_height
        
        if width is not None:
            self.resize(width, self.row_height * 2.5)
            self.row_height = self.width() / self.width_to_row_height
        
        self.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Maximum
        )
        
        self.setStyleSheet("background-color:black")
        
        self.layout = QVBoxLayout()
        
        self.title = QLabel("Notes")
        self.title.resize(self.width(), self.row_height * 1.5)
        
        ##Determining Font sizes
        self.titleFont = self.getFont(self.title.text(), self.title)
        self.titleFont.setBold(1)
        self.noteFont = QFont()
        self.noteFont.setFamily(self.titleFont.family());
        self.noteFont.setPointSize(self.titleFont.pointSize() - 6)
        self.noteFont.setBold(1)
        
        ##Setting Title Font
        self.title.setFont(self.titleFont)
        self.title.setStyleSheet(config.font_colour)

        self.myQListWidget = QListWidget()
        self.myQListWidget.setFrameShape(QFrame.NoFrame)
        self.myQListWidget.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Maximum
        )
        
        self.items = []
        
        #Adding items to layout
        self.layout.addWidget(self.title, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.myQListWidget, alignment=Qt.AlignTop)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        #self.show()        
        self.update(["No items"])
        self.show()

        self.incomingText = "note remove three"
        self.removeNote()
        
        

    def update(self, items):
        self.myQListWidget.clear()
        num_items = len(items)
        if num_items == 0:
            num_items = 1
        self.resize(self.width(), self.row_height * (1.5 + num_items))
        self.layout.setStretchFactor(self.title, 1.5)
        self.layout.setStretchFactor(self.myQListWidget, num_items)
        for i in range(num_items):
            label = QLabel(items[i])
            label.setFixedSize(self.width(), self.row_height)
            label.setFont(self.noteFont)
            label.setStyleSheet(config.font_colour)
            
            item = QListWidgetItem(self.myQListWidget)
            self.myQListWidget.addItem(item)
            self.myQListWidget.setItemWidget(item, label)            

    def addNote(self):
        convertDict = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "to": 2,
            "too": 2
        }
        for i in convertDict.keys():
            self.incomingText = self.incomingText.replace(i, str(convertDict[i]))
        item = self.incomingText[9:]
        self.items.append(item)
        self.update(self.items)
        
    def removeNote(self):
        convertDict = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "to": 2,
            "too": 2
        }
        if self.incomingText[5:6] == "r":
            command = self.incomingText[12:]
            if command == "all" or command == "everything":
                self.items.clear()
                self.update(["No items"])
            else:
                number = convertDict[command]
                try:
                    self.items.pop(number - 1)
                    self.update(self.items)
                except:
                    pass
        elif self.incomingText[5:6] == "c":
            command = self.incomingText[11:]
            if command == "all" or command == "everything":
                self.items.clear()
                self.update(["No items"])
            else:
                number = convertDict[command]
                try:
                    self.items.pop(number - 1)
                    self.update(self.items)
                except:
                    pass
 
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
        return font

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    notes = Notes(width=300)
    notes.show()
    sys.exit(app.exec_())