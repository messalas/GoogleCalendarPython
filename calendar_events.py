import datetime
import pickle
from googleapiclient.discovery import build

CALENDAR_ID = "Enter here the Calendar ID"

transparency_d = dict(busy="opaque", available="transparent")


def create_event(username, title, start, end, description=" ", show_me_as="busy"):
    _validate_params(title, start, end, description, show_me_as)

    token = "tokens/" + username + ".pkl"
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)

    event = dict(
        summary=title,
        start={"date": start, "timeZone": "Europe/Athens"},
        end={"date": end, "timeZone": "Europe/Athens"},
        description=description,
        transparency=transparency_d.get(show_me_as),
        guestsCanInviteOthers=False,
    )
    return service.events().insert(calendarId=CALENDAR_ID, body=event).execute()


def delete_event(username, event_id):
    token = "tokens/" + username + ".pkl"
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)
    service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()


def update_event(username, event_id, title=None, description=None, start=None, end=None, show_me_as=None):
    token = "tokens/" + username + ".pkl"
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

    start = start if start else event["start"]['date']
    end = end if end else event["end"]['date']
    _validate_params(title, start, end, description, show_me_as)

    event["summary"] = title if title else event["summary"]
    event["description"] = description if title else event["description"]
    event["start"]['date'] = start
    event["end"]['date'] = end
    # event["transparency"] = transparency_d.get(show_me_as) if show_me_as else event["transparency"]
    return service.events().update(calendarId=CALENDAR_ID, eventId=event['id'], body=event).execute()


def get_event(username, event_id=None, maxResults=None):
    token = "tokens/" + username + ".pkl"
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


def _validate_params(title, start, end, description, show_me_as):
    if start and end:
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date}")

    if title and not isinstance(title, str):
        raise TypeError("title must be a string")

    if description and not isinstance(description, str):
        raise TypeError("description must be a string")

    if show_me_as and transparency_d.get(show_me_as) is None:
        raise ValueError(f"Invalid value ({show_me_as}) for show_me_as. "
                         f"Accepted values are: {list(transparency_d.keys())}")