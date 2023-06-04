from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.


class Calendar:

    """ Calendar class represents Google Calendar API functionality """

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = 'octassist-cd151aecf343.json'

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH,
            scopes=self.SCOPES
        )
        self.service = build("calendar", "v3", credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            "id": calendar_id
        }
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def add_event(self, calendar_id, body):
        return self.service.events().insert(calendarId=calendar_id, body=body).execute()


obj = Calendar()
calendar = "34d26d5fc687a92669649f6988b8ce852006f604a82e154ef055c991bbb24e49@group.calendar.google.com"

event = {
  'summary': 'Test title',
  'location': 'Kyiv',
  'description': 'Testing adding new event',
  'start': {
    'dateTime': '2023-06-04T14:00:00.000',
    'timeZone': 'GMT+03:00',
  },
  'end': {
    'dateTime': '2023-06-04T17:00:00.000',
    'timeZone': 'GMT+03:00',
  },
}

new_event = obj.add_event(calendar, event)
