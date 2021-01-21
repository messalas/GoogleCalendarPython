import datetime
import pickle
from googleapiclient.discovery import build

CALENDAR_ID =  "Enter here the Calendar ID"

transparency_d = dict(busy="opaque", available="transparent")


def create_event(username, title, start, end, description=" ", show_me_as="busy"):
    """ Creates a google event
    Parameters
    ----------
    username : str,
        The name of the token file located in the "tokens/" directory
        (without the extension '.pkl') that corresponds to a specific user.
    title : str,
        The title of the event
    start : str,
        The starting date of the event. Must be in the form "YYYY-MM-DD"
        e.g. "2021-03-15"
    end :str,
        The ending date of the event. Must be in the form "YYYY-MM-DD"
        e.g. "2021-03-18"
    description : str, (default=" ")
        A small description of the event.
    show_me_as : str, (default="busy")
        If "busy", it leads to "Show me as" to "Busy" in the Calendar UI
        If "available", it leads to "Show me as" to "Available" in the Calendar UI
    Returns
    -------
    created_event : dict
        A dictionary containing information about the created event
    """
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
    """ Deletes an existing event
    Parameters
    ----------
    username : str,
        The name of the token file located in the "tokens/" directory
        (without the extension '.pkl') that corresponds to a specific user.
    event_id : str,
        The id of the event. It exists in the event dictionary under the key "id"
    """
    token = "tokens/" + username + ".pkl"
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)
    service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()


def update_event(username, event_id, title=None, description=None, start=None, end=None, show_me_as=None):
    """ Updates an existing event
    Parameters
    ----------
    username : str,
        The name of the token file located in the "tokens/" directory
        (without the extension '.pkl') that corresponds to a specific user.
    event_id : str,
        The id of the event. It exists in the event dictionary under the key "id"
    title : str (default=None),
        The title of the event
    start : str (default=None),
        The starting date of the event. Must be in the form "YYYY-MM-DD"
        e.g. "2021-03-15"
    end :str (default=None),
        The ending date of the event. Must be in the form "YYYY-MM-DD"
        e.g. "2021-03-18"
    description : str, (default=None)
        A small description of the event.
    show_me_as : str, (default=None)
        If "busy", it leads to "Show me as" to "Busy" in the Calendar UI
        If "available", it leads to "Show me as" to "Available" in the Calendar UI

    Returns
    -------
    updated_event : dict
        A dictionary containing information about the updated event
    """
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
    try:
        event["transparency"] = transparency_d.get(show_me_as) if show_me_as else event["transparency"]
    except KeyError as err:  # Look issue #1
        print(err)
    return service.events().update(calendarId=CALENDAR_ID, eventId=event['id'], body=event).execute()


def _validate_params(title, start, end, description, show_me_as):
    """ Helper function that validates the parameters """
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


def get_event(username, event_id=None, maxResults=None):
    """ Returns a specific event or a number of upcoming events
    Parameters
    ----------
    username : str,
        The name of the token file located in the "tokens/" directory
        (without the extension '.pkl') that corresponds to a specific user.
    event_id : str, (default=None)
        The id of the event. It exists in the event dictionary under the key "id"
    maxResults : int, (default=None)
        The number of upcoming events to return
    Returns
    -------
    A single or a list of events dictionaries
    """
    token = "tokens/" + username + ".pkl"
    credentials = pickle.load(open(token, "rb"))
    service = build('calendar', 'v3', credentials=credentials)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    if event_id and maxResults:
        raise ValueError("event_id and maxResults cannot be set at the same time. Choose one.")

    if event_id:
        return service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

    if maxResults:
        events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                              maxResults=maxResults, singleEvents=True,
                                              orderBy='startTime').execute()
        return events_result.get('items', [])
