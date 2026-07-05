from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.reminder import Reminder
from app.models.application import Application
from app.models.user import User
from app.services.email_service import send_reminder_email

def check_and_send_reminders():
    print(f"[Scheduler] Checking reminders at {datetime.utcnow()} UTC")
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        pending = db.query(Reminder).filter(
            Reminder.is_sent == False,
            Reminder.remind_at <= now
        ).all()

        if not pending:
            print(f"[Scheduler] No pending reminders found.")
            return

        print(f"[Scheduler] Found {len(pending)} pending reminder(s).")

        for reminder in pending:
            try:
                app_obj = db.query(Application).filter(
                    Application.id == reminder.application_id
                ).first()

                if not app_obj:
                    print(f"[Scheduler] Reminder {reminder.id} — application not found, skipping.")
                    reminder.is_sent = True
                    db.commit()
                    continue

                user = db.query(User).filter(User.id == app_obj.user_id).first()

                if not user:
                    print(f"[Scheduler] Reminder {reminder.id} — user not found, skipping.")
                    reminder.is_sent = True
                    db.commit()
                    continue

                print(f"[Scheduler] Sending to {user.email} → {app_obj.company_name} ({reminder.reminder_type})")

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
                    print(f"[Scheduler] ✅ Sent to {user.email}")
                else:
                    print(f"[Scheduler] ❌ Failed for {user.email} — will retry next cycle.")

            except Exception as inner_e:
                # Don't let one failed reminder stop the others
                print(f"[Scheduler] Error processing reminder {reminder.id}: {inner_e}")
                continue

    except Exception as e:
        print(f"[Scheduler] Critical error: {e}")
    finally:
        db.close()

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(check_and_send_reminders, 'interval', minutes=2, max_instances=1, coalesce=True)
    scheduler.start()
    print("[Scheduler] Started — checking reminders every 2 minutes")