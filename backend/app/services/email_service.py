import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_reminder_email(to_email: str, company: str, role: str, reminder_type: str, note: str = None):
    subject = f"Job Tracker Reminder: {reminder_type.replace('_', ' ').title()} for {role} at {company}"

    body = f"""
    Hi there!

    This is your scheduled reminder from Job Tracker.

    Company: {company}
    Role: {role}
    Reminder Type: {reminder_type.replace('_', ' ').title()}
    """
    if note:
        body += f"\nYour note: {note}"

    body += "\n\nLog in to your Job Tracker to update your application status."

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"Email sent to {to_email} for {company} - {role}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False