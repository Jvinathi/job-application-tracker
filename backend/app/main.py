import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, applications, contacts, reminders, stats
from app.services.scheduler import start_scheduler
from app.models import User, Contact, ResumeVersion, Application, Reminder

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API", version="1.0.0")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://job-application-tracker-eosin-one.vercel.app",  # your Vercel URL
    FRONTEND_URL,
]

# Remove duplicates
origins = list(set(origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(applications.router)
app.include_router(contacts.router)
app.include_router(reminders.router)
app.include_router(stats.router)

@app.on_event("startup")
def on_startup():
    start_scheduler()

@app.get("/")
def root():
    return {"message": "Job Tracker API is running!", "docs": "/docs"}