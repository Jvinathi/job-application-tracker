from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.reminder import Reminder
from app.models.application import Application
from app.models.user import User
from app.schemas.reminder import ReminderCreate, ReminderResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/reminders", tags=["Reminders"])
security = HTTPBearer()

def get_current_user_dep(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    return get_current_user(credentials.credentials, db)

@router.get("/", response_model=List[ReminderResponse])
def get_reminders(current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    reminders = db.query(Reminder).join(Application).filter(
        Application.user_id == current_user.id
    ).all()
    return reminders

@router.post("/", response_model=ReminderResponse, status_code=201)
def create_reminder(data: ReminderCreate, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    app_obj = db.query(Application).filter(
        Application.id == data.application_id,
        Application.user_id == current_user.id
    ).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    reminder = Reminder(**data.dict())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

@router.delete("/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: int, current_user: User = Depends(get_current_user_dep), db: Session = Depends(get_db)):
    reminder = db.query(Reminder).join(Application).filter(
        Reminder.id == reminder_id,
        Application.user_id == current_user.id
    ).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    db.delete(reminder)
    db.commit()