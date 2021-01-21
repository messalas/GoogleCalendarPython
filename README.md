# Google Calendar  Python

### Steps for creating a google calendar api:
1. Go to https://console.developers.google.com/ and create a new project. 
2. Go to _OAuth consent screen_ -> select _Internal_ if you have a G suite membership else _External_ 
  - Fill the necesary information 
  - Leave the _Scopes_ section blank (they can be configured in the code)
  - Add the users with their emails that will handle the events (this can be done also later)
3. Go to _Credentials_ -> _Create Credentials_ -> _OAuth client ID_.  Select in the _Application Type_ -> _Desktop App_, name it and click _Create_ 
4. Then go again to _Credentials_ and in the section _OAuth 2.0 Client IDs_ download the json file. 
5. Rename this file to `credentials.json` and put in the projects working directory
6. Go to Library, search for _Google Calendar API_ and then click _ENABLE_

### Saving tokens from users
1. Run `python get_token.py <username>` in terminal and click in the link that appears.
2. The user must then login to his account and give permission to the app to handle events in the calendar for their behalf.
3. After the user has consented, copy the token that appears and paste it into the terminal.
4. After that the token will be saved in the `tokens` folder with the name `<username>.pkl`, where `<username>` is the same one used in 1.

  
### Handling events
- Before using the any method, you must enter the calendar id in the `CALENDAR_ID` variable in [line 5](https://github.com/messalas/GoogleCalendarPython/blob/dd4d026a88fa5b973ec156b40e7568552ac45dd5/calendar_events.py#L5). The calendar id can be found in the information details of the google calendar.

- The first parameter for all the methods  is `username`, which indicates the token from a specific user. You just need to pass the username and not the whole path to the token file (see example below)

Each method has additional parameters

- For the `create` and `update` methods:
  - `title`: the title of the event
  - `start`: the start date of the event. The format of the date must be the following: `"YYYY-MM-DD"` e.g., `"2021-01-15"`
  - `end`: the end date of the event. The format of the date must be the following: `"YYYY-MM-DD"` e.g., `"2021-01-28"`
  - `description`: the description of the event
  - `show_me_as`: `busy` or `available`
  
  For the `delete` and `update` methods:
  - `event_id`: The id of the event.
  
  For the `get` method:
  - `event_id`: returns the event with the given id
  - `maxResults`: returns the given number of upcoming events.
  
 ##### Example for the username="papadopoulos":
 ```python
create_event("papadopoulos", "Άδεια Παπαδόπουλος", "2021-05-15", "2021-05-25", "Μια περιγραφή της άδειας (μπορεί να παραληφθεί)", "busy")

update_event("papadopoulos", title="ΑΔΕΙΑ ΠΑΠΑΔΟΠΟΥΛΟΥ", start="2021-05-13")

 ```
