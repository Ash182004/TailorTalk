from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone
import os

# Absolute path to service account JSON
SERVICE_ACCOUNT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "service_account.json"))
SCOPES = ['https://www.googleapis.com/auth/calendar']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)
CALENDAR_ID = 'primary'

# Define your allowed bookable time slots (24-hour format)
allowed_slots = ["10:00", "14:00", "16:00"]

def check_availability(date_str, start_time=None, end_time=None):
    start_date = datetime.strptime(date_str, "%Y-%m-%d")
    time_min = start_date.isoformat() + 'Z'
    time_max = (start_date + timedelta(days=1)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    busy_slots = []
    for event in events_result.get('items', []):
        start = event['start'].get('dateTime')
        if start:
            time_part = start.split('T')[1][:5]
            busy_slots.append(time_part)
    return busy_slots

def get_free_slots(date_str):
    busy_times = check_availability(date_str)
    free_slots = [slot for slot in allowed_slots if slot not in busy_times]
    return free_slots

def book_slot(date_str, time_str):
    start_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    end_datetime = start_datetime + timedelta(hours=1)
    event = {
        'summary': 'Meeting booked via TailorTalk AI',
        'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event_result.get('htmlLink', None)

def find_event(date_str, time_str):
    # Define start and end of the day in IST
    start_of_day_ist = datetime.strptime(date_str, "%Y-%m-%d").replace(hour=0, minute=0, second=0)
    end_of_day_ist = start_of_day_ist + timedelta(days=1)

    # Convert IST to UTC
    ist_offset = timedelta(hours=5, minutes=30)
    start_of_day_utc = (start_of_day_ist - ist_offset).replace(tzinfo=timezone.utc)
    end_of_day_utc = (end_of_day_ist - ist_offset).replace(tzinfo=timezone.utc)

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_day_utc.isoformat(),
        timeMax=end_of_day_utc.isoformat(),
        singleEvents=True
    ).execute()

    target_time = time_str.strip()

    for event in events_result.get('items', []):
        start = event['start'].get('dateTime')
        if start:
            # Convert event start time to IST for comparison
            event_dt_utc = datetime.fromisoformat(start.replace('Z', '+00:00'))
            event_dt_ist = event_dt_utc + ist_offset
            event_time_str = event_dt_ist.strftime('%H:%M')
            if event_time_str == target_time:
                return [event]

    return []

def cancel_event(date_str, time_str):
    events = find_event(date_str, time_str)
    if events:
        service.events().delete(calendarId=CALENDAR_ID, eventId=events[0]['id']).execute()
        return True
    return False

def reschedule_event(old_date, old_time, new_date, new_time):
    events = find_event(old_date, old_time)
    if events:
        event = events[0]
        new_start = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
        new_end = new_start + timedelta(hours=1)
        event['start']['dateTime'] = new_start.isoformat()
        event['end']['dateTime'] = new_end.isoformat()
        service.events().update(calendarId=CALENDAR_ID, eventId=event['id'], body=event).execute()
        return True
    return False
