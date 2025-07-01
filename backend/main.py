from fastapi import FastAPI, Request
from pydantic import BaseModel
from backend.calendar_utils import get_calendar_service
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
app = FastAPI()

class BookingRequest(BaseModel):
    summary: str
    date: str  # format: YYYY-MM-DD
    time: str  # format: HH:MM (24h)

@app.get("/")
def read_root():
    return {"message": "Calendar Booking API is running!"}

@app.get("/events")
def get_events():
    service = get_calendar_service()
    events_result = service.events().list(
        calendarId=os.getenv("CALENDAR_ID"),
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    formatted = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        formatted.append({"summary": event.get("summary", "No Title"), "start": start})
    return formatted

@app.post("/book")
def book_event(data: BookingRequest):
    service = get_calendar_service()
    start_datetime = f"{data.date}T{data.time}:00"
    end_datetime = (datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S") + timedelta(hours=1)).isoformat()

    event = {
        "summary": data.summary,
        "start": {
            "dateTime": start_datetime,
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": "Asia/Kolkata"
        }
    }

    created_event = service.events().insert(calendarId=os.getenv("CALENDAR_ID"), body=event).execute()
    return {"message": "Booking confirmed!", "eventLink": created_event.get("htmlLink")}
from backend.agent import chat_with_agent

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    reply = chat_with_agent(req.message)
    return {"response": reply}

