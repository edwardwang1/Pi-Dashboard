import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap, QFont, QFontMetrics
from PyQt5.QtCore import QSize
import config

from pyowm import OWM


class Weather(QWidget):
    def __init__(self, parent=None, width=None):
        super(Weather, self).__init__(parent)

        self.pix = QPixmap("")
        self.pic = QLabel(self)
        if width is not None:
            self.w = width
            self.h = self.w * 6 / 4
            self.resize(self.w, self.h)

        self.tempLabel = QLabel("88°C")
        self.humLabel = QLabel("☂ 88%")

        self.highlowLabel = QLabel("88+/88-")

        API_key = 'bd19e6a2d4becb7f55d0f1c39ac0e52e'
        self.owm = OWM(API_key)

        self.initUI()

    def initUI(self):
        self.pic.setPixmap(self.pix)
        self.layout = QGridLayout()
        self.layout.addWidget(self.pic, 1, 1, 4, 4, Qt.AlignCenter)
        self.layout.addWidget(self.tempLabel, 5, 1, 2, 2, Qt.AlignLeft)
        self.layout.addWidget(self.humLabel, 5, 3, 1, 2, Qt.AlignRight)
        self.layout.addWidget(self.highlowLabel, 6, 3, 1, 2, Qt.AlignRight)

        self.setLayout(self.layout)

        self.resizeComponents()

        self.getWeather()
        self.setStyleSheet("background-color: black")
        self.show()
        
        print("weather", self.width(), self.height())

    def getWeather(self):
        obs = self.owm.weather_at_place("Vancouver")
        w = obs.get_weather()

        tempDict = w.get_temperature(unit="celsius")
        self.status = w.get_status()
        self.status = self.status.lower()
        humidity = w.get_humidity()
        self.temp = str(round(tempDict['temp'])) + "°C"
        self.temp_max = str(round(tempDict['temp_max']))
        self.temp_min = str(round(tempDict['temp_min']))
        self.hum = "☂ " + str(round(humidity)) + "%"

        print(self.temp, self.status)
        self.displayWeather()

    def resizeComponents(self):
        #Resizing
        self.pic.resize(int(self.width()), int(self.width()))
        self.tempLabel.resize(int(self.width() / 2), int(self.width() / 2))
        self.humLabel.resize(int(self.width() / 2), int(self.width() / 4))
        self.highlowLabel.resize(int(self.width() / 2), int(self.width() / 4))

        for item in self.humLabel, self.highlowLabel:
            item.setFont(self.getFont(self.humLabel.text(), self.humLabel))
            item.setStyleSheet(config.font_colour)

        self.tempLabel.setFont(self.getFont(self.tempLabel.text(), self.tempLabel))
        self.tempLabel.setStyleSheet(config.font_colour)

    def displayWeather(self):       #
        self.tempLabel.setText(self.temp)
        self.humLabel.setText(self.hum)
        self.highlowLabel.setText(self.temp_max + "+/" + self.temp_min + "-")

        width = int(self.pic.width() * .85)
        height = int(self.pic.height() * .85)
        onPi = True
        
        if onPi is False:
            if "sun" in self.status:
                self.pix = QPixmap("icons/clear.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "rain" in self.status or "shower" in self.status:
                self.pix = QPixmap("icons/rainy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "snow" in self.status or "hail" in self.status:
                self.pix = QPixmap("icons/rainy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "storm" in self.status or "lightning" in self.status:
                self.pix = QPixmap("icons/rainy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "mist" in self.status:
                self.pix = QPixmap("icons/rainy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "cloud" in self.status:
                self.pix = QPixmap("icons/cloudy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            else:
                self.pix = QPixmap("icons/cloudy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)
        else:
            if "sun" in self.status:
                self.pix = QPixmap("/home/pi/Desktop/RPiDashboard/icons/clear.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "rain" in self.status or "shower" in self.status:
                self.pix = QPixmap("/home/pi/Desktop/RPiDashboard/icons/rainy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "snow" in self.status or "hail" in self.status:
                self.pix = QPixmap("/home/pi/Desktop/RPiDashboard/icons/rainy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "storm" in self.status or "lightning" in self.status:
                self.pix = QPixmap("/home/pi/Desktop/RPiDashboard/icons/rainy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "mist" in self.status:
                self.pix = QPixmap("/home/pi/Desktop/RPiDashboard/icons/rainy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            elif "cloud" in self.status:
                self.pix = QPixmap("/home/pi/Desktop/RPiDashboard/icons/cloudy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)

            else:
                self.pix = QPixmap("/home/pi/Desktop/RPiDashboard/icons/cloudy.png")
                self.pix = self.pix.scaled(width, height)
                self.pic.setPixmap(self.pix)


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
                wouldfit = max(fs - 4, 1)
                font.setPointSize(wouldfit)
                break
        font.setFamily(config.font_family)
        font.setBold(1)
        return font


def main():
    app = QApplication(sys.argv)
    main = Weather(width=250)
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    print("tset")
