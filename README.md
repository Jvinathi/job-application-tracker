# Job Application Tracker

A full-stack productivity app to manage job applications with a Kanban board, automated email reminders, and pipeline analytics.

## Features
- Drag-and-drop Kanban board (Applied → Shortlisted → Interview → Offer / Rejected)
- JWT authentication (register/login)
- Automated follow-up email reminders (APScheduler + Gmail SMTP)
- Stats dashboard: response rate, offer rate, pipeline breakdown
- Contact and resume version tracking

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite, Tailwind CSS, @dnd-kit, Recharts |
| Backend | Python, FastAPI, SQLAlchemy ORM |
| Database | MySQL |
| Auth | JWT (python-jose) + bcrypt |
| Scheduler | APScheduler |
| Email | smtplib (Gmail SMTP, free) |

## Run Locally

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

Live App  → https://job-application-tracker-black-nu.vercel.app

API Docs  → https://job-application-tracker-production-6316.up.railway.app
