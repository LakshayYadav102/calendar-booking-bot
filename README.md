# 📅 Calendar Booking Chatbot

A conversational AI agent that helps users schedule appointments on their Google Calendar through a seamless chat interface.

This project uses natural language understanding to interpret user requests, checks for available time slots, and books events — all automatically through conversation.

---

## 🚀 Live Links

- 🔗 **Frontend (Streamlit App)**: [https://calendar-booking-bot-dvhfappbr59kbyrrtvzkajc.streamlit.app/](https://calendar-booking-bot-dvhfappbr59kbyrrtvzkajc.streamlit.app/)
- 🔗 **Backend (FastAPI on Render)**: [https://calendar-backend-gxmj.onrender.com](https://calendar-backend-gxmj.onrender.com)

---

## ✅ Features

- 📆 Book Google Calendar events through chat
- 🧠 Natural language understanding via LLM (e.g., Gemini)
- 🔁 Back-and-forth conversation for clarification
- 🛠 Function calling using LangChain/LangGraph
- 🔐 Uses Google Calendar API via Service Account
- 🌐 Fully hosted on Streamlit and Render

---

## 🧰 Tech Stack

| Layer       | Technology                         |
|-------------|-------------------------------------|
| Frontend    | Streamlit                          |
| Backend     | FastAPI                            |
| LLM Agent   | LangGraph + LangChain              |
| Calendar API| Google Calendar (Service Account)  |
| LLM Model   | Gemini / Grok (via API)            |
| Hosting     | Render (Backend), Streamlit Cloud (Frontend) |

---

## 🗂 Project Structure
calendar-booking-bot/
│
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── agent.py # LangChain/LangGraph agent logic
│ └── google_calendar_tool.py# Tool for Google Calendar integration
│
├── frontend/
│ └── app.py # Streamlit chat interface
│
├── requirements.txt # Dependencies
├── render.yaml # Render deployment configuration
└── README.md # Project documentation

## ⚙️ Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- Google Cloud Service Account with Calendar API enabled
- Calendar created and shared with the Service Account
- `.env` file for backend with:


### 2. Backend (FastAPI + LangChain)

```bash
cd backend/
pip install -r ../requirements.txt
uvicorn main:app --reload

Frontend (Streamlit)
bash
Copy
Edit
cd frontend/
streamlit run app.py
