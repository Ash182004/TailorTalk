from app.calendar_utils import get_free_slots, book_slot, cancel_event, reschedule_event
from datetime import datetime
import dateparser
import re

def parse_date(input_text):
    # Handle "on 29" type inputs
    day_match = re.search(r'\bon\s+(\d{1,2})\b', input_text.lower())
    if day_match:
        day = int(day_match.group(1))
        today = datetime.today()
        month = today.month
        year = today.year
        # If day has already passed this month, assume next month
        if day < today.day:
            month += 1
            if month > 12:
                month = 1
                year += 1
        try:
            dt = datetime(year, month, day)
            return dt.strftime('%Y-%m-%d')
        except:
            pass  # Ignore invalid dates (like Feb 30)

    # Fallback to normal dateparser
    dt = dateparser.parse(input_text, settings={'PREFER_DATES_FROM': 'future'})
    if dt:
        return dt.strftime('%Y-%m-%d')
    return None

def parse_time(input_text):
    match = re.search(r'\b(\d{1,2}):(\d{2})\b', input_text)
    if match:
        return match.group()
    match2 = re.search(r'\b(\d{1,2})(am|pm)\b', input_text, re.IGNORECASE)
    if match2:
        hour = int(match2.group(1))
        if 'pm' in match2.group(2).lower() and hour != 12:
            hour += 12
        return f"{hour:02d}:00"
    return None

def parse_intent(user_input):
    text = user_input.lower()
    if any(greet in text for greet in ["hi", "hello", "hey"]):
        return "greeting"
    if "availability" in text or "free time" in text or "slots" in text:
        return "check_availability"
    if "book" in text or "schedule" in text:
        return "book_slot"
    if "cancel" in text:
        return "cancel"
    if "reschedule" in text:
        return "reschedule"
    return "fallback"

def chat_response(user_input, session_state):
    intent = parse_intent(user_input)
    date = parse_date(user_input) or datetime.today().strftime('%Y-%m-%d')
    time = parse_time(user_input)

    if intent == "greeting":
        return "Hello! I can help with checking availability, booking, rescheduling, or cancelling meetings."

    elif intent == "check_availability":
        slots = get_free_slots(date)
        if slots:
            return f"Available slots on {date}: {', '.join(slots)}"
        else:
            return f"No available slots on {date}."

    elif intent == "book_slot":
        slots = get_free_slots(date)
        selected_time = time if time else (slots[0] if slots else None)
        if selected_time and selected_time not in slots:
            return f"Sorry, {selected_time} is not available."
        if selected_time:
            link = book_slot(date, selected_time)
            return f"Your meeting is booked at {selected_time} on {date}. View here: {link}"
        else:
            return "No slots available to book."

    elif intent == "cancel":
        if time:
            success = cancel_event(date, time)
            return "Meeting cancelled." if success else "No meeting found at that time to cancel."
        else:
            return "Please specify the time of the meeting you want to cancel."

    elif intent == "reschedule":
        times = re.findall(r'(\d{1,2}:\d{2})', user_input)
        if len(times) == 2:
            success = reschedule_event(date, times[0], date, times[1])
            return "Meeting rescheduled." if success else "Could not reschedule. Meeting not found."
        else:
            return "Please specify both old and new times for rescheduling."

    else:
        return "I can help check availability, book, reschedule, or cancel meetings. What would you like to do?"
