from google.oauth2 import service_account
from googleapiclient.discovery import build

from dotenv import load_dotenv

import datetime

# If modifying these scopes, delete the file token.json.


class GoogleCalendar:

    """ Calendar class represents Google Calendar API functionality.
    Requires a calendarId as argument"""

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # Path to service_account.json file
    SERVICE_MAIL_FILE = 'google_calendar/service_mail.json'

    def __init__(self, calendar_id):
        self.credentials = service_account.Credentials.from_service_account_file(
            filename=self.SERVICE_MAIL_FILE,
            scopes=self.SCOPES
        )
        self.service = build("calendar", "v3", credentials=self.credentials)
        self.calendar_id = calendar_id

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self):
        calendar_list_entry = {
            "id": self.calendar_id
        }
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def add_event(self, customer_name, session_description, date: str, time: str, **kwargs):

        """ Adds an event to an Administrator calendar.
        customer_name - used to build an event info card
        session_description - used to build an event session purpose (service type)
        date - passes in format 'month-day' (05-25). Parses and hands over to method for event booking
        time - time to book an event.
        """

        time = time.split(":")

        hour, minutes = time[0], time[1]

        event = {
            'summary': f'{customer_name}',
            'location': 'Kyiv',
            'description': f'{session_description}',
            'start': {
                'dateTime': f'{datetime.date.today().year}-{date}T{hour}:{minutes}:00.000',
                'timeZone': 'GMT+3:00',
            },
            'end': {
                'dateTime': f'{datetime.date.today().year}-{date}T{int(hour)+2}:{minutes}:00.000',
                'timeZone': 'GMT+3:00',
            },
            ** kwargs
        }

        return self.service.events().insert(calendarId=self.calendar_id, body=event).execute()

    def list_events(self):
        return self.service.events().list(calendarId=self.calendar_id).execute()

    def get_event_hours(self, date: str, available=False):

        """
        List a booked events hours for a date given as argument.
        date - date in format 'month-day' ('05-25' as example)
        if available = True, gives an available hours instead
        """

        start_time = f'{datetime.date.today().year}-{date}T08:00:00+03:00'
        end_time = f'{datetime.date.today().year}-{date}T18:00:00+03:00'

        events = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=start_time,
            timeMax=end_time,
            timeZone='GMT+3:00'
        ).execute()

        event_data = events['items']
        time_booked = []
        for event in event_data:
            # Weird line of code to split DateTime string to bring it to human-readable representation
            event_obj = event['start']['dateTime'].split("T")[1].split("+")[0]
            time_booked.append(event_obj[0:5])
        print(time_booked)

        if available:
            all_hours = {"08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"}
            booked_hours = set(time_booked)

            # Calculating occupied hours
            occupied_hours = set()
            for booked_time in booked_hours:
                occupied_hours.add(booked_time)
                hour, minutes = booked_time.split(":")
                occupied_hours.add(f"{int(hour) + 1:02d}:{minutes}")
            available_hours = list(all_hours - occupied_hours)
            return sorted(available_hours, key=lambda x: int(x[0:2]))

        else:
            return time_booked
