from datetime import datetime, timedelta
from twilio.rest import Client
from django.conf import settings
from .models import OpeningHours

def generate_time_slots(start_time, end_time):
    time_slots = []
    current_time = start_time
    while current_time < end_time:
        end_current_slot = current_time + timedelta(hours=1)
        time_slot = f"{current_time.strftime('%H:%M')}-{end_current_slot.strftime('%H:%M')}"
        time_slots.append(time_slot)
        current_time = end_current_slot
    return time_slots

def fetch_available_times(selected_date):
    weekday = selected_date.weekday()
    try:
        opening_hours = OpeningHours.objects.get(day_of_week=weekday)
    except OpeningHours.DoesNotExist:
        return []  # No opening hours for this day

    start_time = datetime.combine(selected_date, opening_hours.start_time)
    end_time = datetime.combine(selected_date, opening_hours.end_time)
    
    if start_time > end_time:
        end_time += timedelta(days=1)  # Handle cases where end_time is on the next day

    return generate_time_slots(start_time, end_time)

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
phone_number = settings.TWILIO_PHONE_NUMBER

client = Client(account_sid, auth_token)

def send_sms(reciever_phone_number, reservation):
    try:
        message_body = f"Your reservation has been confirmed at {reservation.date} {reservation.time}. If you want to change or cancel this reservation click here: https://bellaitaliarestaurant-bfa3d8f4d24e.herokuapp.com/accounts/profile/"
        message = client.messages.create(
            body=message_body,
            from_=phone_number,
            to=reciever_phone_number
        )
        print(f"Message sent successfully! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        return False
