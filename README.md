# TailorTalk Advanced Plus - Calendar Booking AI 🚀

## ✅ Features Included:
- Greeting Handling
- Check Availability (date + time range)
- Book Meeting (today, tomorrow, specific dates)
- Reschedule Meetings
- Cancel Meetings
- Natural Language Date & Time Parsing (using dateparser)
- Streamlit Chat UI

## ✅ Setup Instructions:



2. Create virtual environment:
```bash
python -m venv venv
# Windows:
.env\Scriptsctivate
# Mac/Linux:
source venv/bin/activate
```

3. Install packages:
```bash
pip install -r requirements.txt
```

4. Place your Google service_account.json inside:
```
app/service_account.json
```

5. Run FastAPI backend:
```bash
cd ..
uvicorn main:app --reload
```

6. Run Streamlit frontend (new terminal):
```bash
cd frontend
streamlit run streamlit_app.py
```

7. Open: http://localhost:8501

## ✅ Sample Inputs to Try:
- "Hi"
- "What slots are free today?"
- "Book a meeting at 3 PM today"
- "Cancel my 2 PM meeting today"
- "Reschedule my 10 AM meeting today to 11 AM"
- "Book a slot next Friday at 4 PM"

## ✅ Notes:
- Make sure your Google Calendar is shared with your service account email.
- Google Calendar API must be enabled in Google Cloud Console.
