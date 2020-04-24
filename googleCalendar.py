from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import config

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QFont, QFontMetrics

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
tz = config.tz

max_today_events = 5
max_week_events = 10


class GoogleCalendar(QWidget):
    def __init__(self, width=None, parent=None):
        self.width_to_row_height = 11
        super(GoogleCalendar, self).__init__(parent)

        if width is not None:
            self.resize(width, self.height())

        self.todayLabel = QLabel("Today's Events")
        self.weekLabel = QLabel("This Week's Events")
        self.todayEvents = QLabel("test events \n test events")
        self.weekEvents = QLabel("test events \n test events")

        self.setStyleSheet("background-color: black")

        self.calendarLayout = QVBoxLayout()
        self.row_height = self.width() / self.width_to_row_height

        # resizing title labels and setting fonts
        for item in self.todayLabel, self.weekLabel:
            item.resize(self.width(), self.row_height * 1.5)
        self.titleFont = self.getFont(self.todayLabel.text(), self.todayLabel)
        self.titleFont.setBold(1)
        self.eventFont = QFont()
        self.eventFont.setFamily(self.titleFont.family());
        self.eventFont.setPointSize(self.titleFont.pointSize() - 6)
        for item in self.todayLabel, self.weekLabel:
            item.setFont(self.titleFont)
            item.setStyleSheet(config.font_colour)

        for item in self.todayEvents, self.weekEvents:
            item.setFont(self.eventFont)
            item.setStyleSheet(config.font_colour)

        self.calendarLayout.addWidget(self.todayLabel)
        self.calendarLayout.addWidget(self.todayEvents)
        self.calendarLayout.addWidget(self.weekLabel)
        self.calendarLayout.addWidget(self.weekEvents)

        self.setLayout(self.calendarLayout)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000 * 60 * 60)

        self.update()
        self.show()

    def resize_rows(self, num_today_events, num_week_events):
        self.resize(self.width(), self.row_height * (2 + num_today_events + num_week_events))
        self.todayEvents.resize(self.width(), self.row_height * num_today_events)
        self.weekEvents.resize(self.width(), self.row_height * num_week_events)

    def update(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Gathering events from all calendars
        page_token = None
        all_events = []
        now = datetime.datetime.utcnow()
        now_iso = now.isoformat() + 'Z'  # 'Z' indicates UTC time
        max_time = now + datetime.timedelta(days=7)
        max_time = max_time.isoformat() + 'Z'
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                all_events.append(
                    service.events().list(calendarId=calendar_list_entry['id'], timeMin=now_iso, timeMax=max_time,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute())

            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        event_starts = []
        descriptions = []
        for e in all_events:
            events = e.get('items', [])
            for event in events:
                event_starts.append(event['start'].get('dateTime', event['start'].get('date')))
                descriptions.append(event['summary'])

        # sorting based on starting times
        for i in range(len(event_starts)):
            if len(event_starts[i]) > 10:
                # converting to UTC and removing time zone
                event_starts[i] = event_starts[i][:22] + event_starts[i][23:]
                event_starts[i] = datetime.datetime.strptime(event_starts[i], "%Y-%m-%dT%H:%M:%S%z")
                event_starts[i] = event_starts[i].astimezone(datetime.timezone.utc)
                event_starts[i] = event_starts[i].replace(tzinfo=None)

            else:
                # for all day events
                event_starts[i] = datetime.datetime.strptime(event_starts[i], "%Y-%m-%d")

        descriptions = [x for _, x in sorted(zip(event_starts, descriptions), key=lambda pair: pair[0])]
        event_starts.sort()

        today = now.replace(tzinfo=datetime.timezone.utc)
        today = today.astimezone(tz).date()
        # after sorting, converting back to appropriate time zone
        today_events_idxs = []
        for i in range(len(event_starts)):
            event_starts[i] = event_starts[i].replace(tzinfo=datetime.timezone.utc)
            event_starts[i] = event_starts[i].astimezone(tz)
            if (event_starts[i].date() == today):
                today_events_idxs.append(i)

        # filling out widget
        today_counter = 0
        week_counter = 0
        today_str = ""
        week_str = ""
        num_today_events = len(today_events_idxs)
        num_week_events = len(event_starts) - num_today_events
        if num_today_events == 0:
            today_str = "No events today"
            num_today_events = 1
        if num_week_events == 0:
            week_str = "No upcoming events"
            num_week_events = 1
        for i in range(len(event_starts)):
            if i in today_events_idxs:
                if today_counter < max_today_events:
                    today_counter += 1
                    today_str += ((event_starts[i].strftime("%I:%M %p") + "  " + descriptions[i]) + "\n")
            else:
                if week_counter < max_week_events:
                    week_counter += 1
                    week_str += ((event_starts[i].strftime("%b %d") + "      " + descriptions[i]) + "\n")

        if today_str[-1] == "\n":
            today_str = today_str[:-1]

        if week_str[-1] == "\n":
            week_str = week_str[:-1]

        self.todayEvents.setText(today_str)
        self.weekEvents.setText(week_str)

        self.resize_rows(num_today_events, num_week_events)

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
    calendar = GoogleCalendar()
    calendar.show()
    sys.exit(app.exec_())
