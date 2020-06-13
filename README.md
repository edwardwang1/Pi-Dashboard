# Pi-Dashboard

This dashboard is designed to be run on Raspberry Pi 3. While the dashboard can be run standalone, it was built to interact with [Mycroft](https://mycroft.ai/), an open source voice assistant. To do so, the Mycroft skill: skill-dashboard must be installed. See the [Github repo](https://github.com/edwardwang1/skill-dashboard) for additional details. 

## Dependencies
Install the [Google Client Library](https://developers.google.com/calendar/quickstart/python):

`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

Install [PyOWM](https://pyowm.readthedocs.io/en/latest/):

`pip install pyowm`

Install [Pyro4](https://pypi.org/project/Pyro4/):

`pip install Pyro4`

Install [PyQt5](https://pypi.org/project/PyQt5/):

`pip install PyQt5`

For any remaining packages, `pip install package` should do the trick.

## Using the Google Calendar API

If you want to use the calendar widget, you will need enable the Google Calendar API and download the credentials.json file into the main directory. Follow the instructions [here](https://developers.google.com/calendar/quickstart/python).

## Weather Icon attributions
The weather icons were downloaded from [The Noun Project](https://thenounproject.com/)

clear.png Author: [Sébastien Robaszkiewicz](https://thenounproject.com/icon/408567/)

cloudy.png Author: [hunotika](https://thenounproject.com/icon/42745/)

misty.png Author: [P Thanga Vignesh](https://thenounproject.com/icon/217683/)

rainy.png Author: [Jen Maestas](https://thenounproject.com/icon/97498/)

snowy.png Author: [Edward Boatman](https://thenounproject.com/icon/426/)

stormy.png Author: [Ji Sub Jeong](https://thenounproject.com/icon/68577/)

## Features 
* Digital clock
* Events widget that displays events from Google Calendar
* Weather widget using data from PyOWM
* Notes Widget (reqiures Mycroft to trigger events)
* Command display that displays the utterance heard by Mycroft
