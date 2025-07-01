import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.api_core.exceptions import ResourceExhausted

from backend.calendar_utils import get_calendar_service

# Load environment variables
load_dotenv()

# Configure Google GenAI with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def book_event(summary: str, date: str, time: str) -> str:
    service = get_calendar_service()
    start_datetime = f"{date}T{time}:00"
    end_datetime = (datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S") + timedelta(hours=1)).isoformat()

    event = {
        "summary": summary,
        "start": {"dateTime": start_datetime, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_datetime, "timeZone": "Asia/Kolkata"}
    }

    created_event = service.events().insert(calendarId=os.getenv("CALENDAR_ID"), body=event).execute()
    return f"✅ Booking confirmed for '{summary}' on {date} at {time}. [View Event]({created_event.get('htmlLink')})"

def book_event_via_prompt(prompt: str):
    # Try natural language format
    match = re.search(r"'(.+)' on (\d{4}-\d{2}-\d{2}) at (\d{2}:\d{2})", prompt)
    if match:
        summary, date, time = match.groups()
        return book_event(summary, date, time)
    
    # Try structured format
    structured_match = re.search(r"title='(.+?)', date='(\d{4}-\d{2}-\d{2})', time='(\d{2}:\d{2})'", prompt)
    if structured_match:
        summary, date, time = structured_match.groups()
        return book_event(summary, date, time)
    
    return "❌ Couldn't extract booking info. Try: 'Book event titled 'Meeting' on 2025-07-02 at 14:00' or structured format like title='Meeting', date='2025-07-02', time='14:00'"

tools = [
    Tool(
        name="BookCalendarEvent",
        func=lambda query: book_event_via_prompt(query),
        description="Use this to book Google Calendar events. Input should include title, date (YYYY-MM-DD), and time (HH:MM). Example: 'Book event titled 'Meeting' on 2025-07-02 at 14:00' or structured format like title='Meeting', date='2025-07-02', time='14:00'."
    )
]

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Create LangChain agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=120),
    retry=retry_if_exception_type(ResourceExhausted)
)
def chat_with_agent(user_message: str):
    return agent_executor.invoke({"input": user_message})["output"]