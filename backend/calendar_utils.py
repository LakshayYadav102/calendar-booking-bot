from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
print("GOOGLE_APPLICATION_CREDENTIALS =", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
print("CALENDAR_ID =", os.getenv("CALENDAR_ID"))

def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        scopes=["https://www.googleapis.com/auth/calendar"]
    )
    return build("calendar", "v3", credentials=creds)

def list_upcoming_events():
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId=os.getenv("CALENDAR_ID"),
        maxResults=5,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    events = events_result.get('items', [])
    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))  # fallback to date
        summary = event.get('summary', 'No Title')
        print(summary, start)

# Run this test
if __name__ == "__main__":
    list_upcoming_events()
