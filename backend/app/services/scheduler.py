from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.reminder import Reminder
from app.models.application import Application
from app.models.user import User
from app.services.email_service import send_reminder_email

def check_and_send_reminders():
    print(f"[Scheduler] Checking reminders at {datetime.now()}")
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        pending = db.query(Reminder).filter(
            Reminder.is_sent == False,
            Reminder.remind_at <= now
        ).all()

        for reminder in pending:
            app_obj = db.query(Application).filter(Application.id == reminder.application_id).first()
            if not app_obj:
                continue
            user = db.query(User).filter(User.id == app_obj.user_id).first()
            if not user:
                continue

            success = send_reminder_email(
                to_email=user.email,
                company=app_obj.company_name,
                role=app_obj.role_title,
                reminder_type=reminder.reminder_type,
                note=reminder.note
            )
            if success:
                reminder.is_sent = True
                db.commit()
    finally:
        db.close()

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=15)
    scheduler.start()
    print("[Scheduler] Started — checking reminders every 15 minutes")