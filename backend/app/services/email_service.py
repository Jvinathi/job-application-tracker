import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_reminder_email(to_email: str, company: str, role: str, reminder_type: str, note: str = None):
    subject = f"[Job Tracker] Reminder: {reminder_type.replace('_', ' ').title()} — {role} at {company}"

    # Plain text version
    plain_body = f"""Hi there!

This is your scheduled reminder from Job Tracker.

Company  : {company}
Role     : {role}
Reminder : {reminder_type.replace('_', ' ').title()}
"""
    if note:
        plain_body += f"\nYour note: {note}\n"
    plain_body += "\nLog in to Job Tracker to update your application status."

    # HTML version — looks professional, less likely to hit spam
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px;">
        <div style="background: #1E40AF; padding: 20px; border-radius: 8px 8px 0 0;">
            <h2 style="color: white; margin: 0;">Job Tracker Reminder</h2>
        </div>
        <div style="background: #f8fafc; padding: 24px; border: 1px solid #e2e8f0; border-radius: 0 0 8px 8px;">
            <p style="color: #334155; font-size: 15px;">Hi there! Here is your scheduled reminder:</p>
            <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
                <tr style="background: #e2e8f0;">
                    <td style="padding: 10px 14px; font-weight: bold; color: #1e293b; width: 35%;">Company</td>
                    <td style="padding: 10px 14px; color: #334155;">{company}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 14px; font-weight: bold; color: #1e293b;">Role</td>
                    <td style="padding: 10px 14px; color: #334155;">{role}</td>
                </tr>
                <tr style="background: #e2e8f0;">
                    <td style="padding: 10px 14px; font-weight: bold; color: #1e293b;">Reminder</td>
                    <td style="padding: 10px 14px; color: #334155;">{reminder_type.replace('_', ' ').title()}</td>
                </tr>
                {'<tr><td style="padding: 10px 14px; font-weight: bold; color: #1e293b;">Your Note</td><td style="padding: 10px 14px; color: #334155;">' + note + '</td></tr>' if note else ''}
            </table>
            <div style="margin-top: 20px; padding: 14px; background: #dbeafe; border-radius: 6px;">
                <p style="margin: 0; color: #1e40af; font-size: 14px;">
                    Log in to your Job Tracker to update your application status.
                </p>
            </div>
            <p style="color: #94a3b8; font-size: 12px; margin-top: 24px;">
                You set this reminder yourself in Job Tracker. 
                To stop receiving reminders, delete them from the app.
            </p>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['From'] = f"Job Tracker <{EMAIL_ADDRESS}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['X-Mailer'] = 'Job Tracker App'

    # Attach both plain and HTML — Gmail uses HTML, spam filters prefer seeing both
    msg.attach(MIMEText(plain_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False