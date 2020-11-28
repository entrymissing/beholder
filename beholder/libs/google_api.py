import datetime
import os.path
import pickle
from googleapiclient.discovery import build
from googleapiclient import errors

SCOPES = ('https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/fitness.activity.read')

def build_service(service_name, version, pickle_path=None):
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    if not pickle_path:
        home_dir = os.path.expanduser('~')
        pickle_path = os.path.join(home_dir, '.credentials', 'token.pkl')
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            creds = pickle.load(token)
    service = build(service_name, version, credentials=creds)
    return service

def list_mails_matching_query(service, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId='me',
                                                   q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return []

def get_message(service, msg_id):
    """Get a Message with given ID.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: The ID of the Message required.

    Returns:
      A Message.
    """
    try:
        message = service.users().messages().get(userId='me', id=msg_id).execute()
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def get_calendar_by_name(service, name):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == name:
                return calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    return None

def get_calendar_entries_by_query(service, query, num_hours, calendar_name):
    # Find the right calendar
    calendar_id = get_calendar_by_name(service, calendar_name)

    # Compute some timestamps
    utcnow = datetime.datetime.utcnow()
    ndays = utcnow - datetime.timedelta(hours=num_hours)
    # 'Z' indicates UTC time
    utcnow = utcnow.isoformat() + 'Z'
    ndays = ndays.isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=calendar_id, timeMin=ndays, timeMax=utcnow, q=query, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events
