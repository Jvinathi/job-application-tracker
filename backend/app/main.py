import os
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.routers import auth, applications, contacts, reminders, stats
from app.services.scheduler import start_scheduler
from app.models import User, Contact, ResumeVersion, Application, Reminder

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler — logs every 500 error with full traceback
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_detail = traceback.format_exc()
    print(f"[ERROR] 500 on {request.method} {request.url}")
    print(f"[ERROR] {error_detail}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": error_detail},
        headers={"Access-Control-Allow-Origin": "*"}
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