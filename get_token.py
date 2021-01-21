import sys
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def get_token(username):
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES)
    credentials = flow.run_console()
    pickle.dump(credentials, open(f"tokens/{username}.pkl", "wb"))


if __name__ == '__main__':
    command_line_args = sys.argv
    if len(command_line_args) > 2:
        raise ValueError("Please provide only one username in the command line.")

    get_token(str(command_line_args[1]))

    print("\n\n Token has been successfully saved.")