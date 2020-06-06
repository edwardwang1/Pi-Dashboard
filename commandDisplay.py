from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,  QLabel, QWidget, QVBoxLayout, QSizePolicy
from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QFontMetrics
import config


class CommandDisplay(QWidget):
    def __init__(self, width=None, parent=None):    
        super(CommandDisplay, self).__init__(parent)
        
        self.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Maximum
        )
        
        if width is not None:
            self.resize(width, width/6)
            
        self.inputLabel = QLabel("Command")
        self.inputLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.inputLabelFont = QFont()
        self.inputLabelFont.setFamily(config.font_family)
        self.inputLabelFont.setPointSize(18)
        self.inputLabel.setFont(self.inputLabelFont)
        self.inputLabel.setStyleSheet(config.font_colour)
        self.show()
        
        self.displayLayout = QVBoxLayout()
        self.displayLayout.addWidget(self.inputLabel)        
        self.setLayout(self.displayLayout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    display = CommandDisplay()
    display.show()
    sys.exit(app.exec_())
