import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CALENDAR_ID = "77u6oodmpu3ov6ree22iodln3s@group.calendar.google.com"   # Enter here the Calendar ID


def get_token(username):
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES)
    credentials = flow.run_console()
    pickle.dump(credentials, open(f"{username}.pkl", "wb"))


def create_event(token, title, description, start, end, transparency):
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)

    event = dict()
    event.setdefault("summary", title)
    event.setdefault("description", description)
    event.setdefault("start", {"date": start, "timeZone": "Europe/Athens"})
    event.setdefault("end", {"date": end, "timeZone": "Europe/Athens"})
    event.setdefault("transparency", transparency)
    event.setdefault("guestsCanInviteOthers", False)

    event.setdefault("reminders", {
        'useDefault': False,  'overrides': [{'method': 'email', 'minutes': 24 * 60}]
    })
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()


def delete_event(token, event_id):
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)
    service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()


def update_event(token, event_id, title=None, description=None, start=None, end=None, transparency=None):
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

    event["summary"] = title if title else event["summary"]
    event["description"] = description if title else event["description"]
    event["start"]['date'] = start if start else event["start"]['date']
    event["end"]['date'] = end if end else event["end"]['date']
    event["transparency"] = transparency if transparency else event["transparency"]
    service.events().update(calendarId=CALENDAR_ID, eventId=event['id'], body=event).execute()


def get_event(token, event_id=None, maxResults=None):
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    if event_id:
        return service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

    if maxResults:
        events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                              maxResults=maxResults, singleEvents=True,
                                              orderBy='startTime').execute()
        return events_result.get('items', [])


